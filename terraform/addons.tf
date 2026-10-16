# Required for the PostgreSQL PVC and backend CPU-based HPA on EKS.
# Pod Identity grants storage permissions to the CSI controller, not all nodes.
resource "aws_eks_addon" "pod_identity" {
  cluster_name  = aws_eks_cluster.this.name
  addon_name    = "eks-pod-identity-agent"
  addon_version = "v1.3.10-eksbuild.3"
  depends_on    = [aws_eks_node_group.this]
  tags          = { Project = "relaydesk-capstone" }
}

resource "aws_iam_role" "ebs_csi" {
  name = "${var.name}-ebs-csi-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "pods.eks.amazonaws.com" }
      Action    = ["sts:AssumeRole", "sts:TagSession"]
      Condition = { StringEquals = {
        "aws:RequestTag/kubernetes-namespace"       = "kube-system"
        "aws:RequestTag/kubernetes-service-account" = "ebs-csi-controller-sa"
      } }
    }]
  })
  tags = { Project = "relaydesk-capstone" }
}

resource "aws_iam_role_policy_attachment" "ebs_csi" {
  role       = aws_iam_role.ebs_csi.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
}

resource "aws_eks_pod_identity_association" "ebs_csi" {
  cluster_name    = aws_eks_cluster.this.name
  namespace       = "kube-system"
  service_account = "ebs-csi-controller-sa"
  role_arn        = aws_iam_role.ebs_csi.arn
  depends_on      = [aws_eks_addon.pod_identity, aws_iam_role_policy_attachment.ebs_csi]
  tags            = { Project = "relaydesk-capstone" }
}

resource "aws_eks_addon" "ebs_csi" {
  cluster_name  = aws_eks_cluster.this.name
  addon_name    = "aws-ebs-csi-driver"
  addon_version = "v1.67.0-eksbuild.1"
  depends_on    = [aws_eks_pod_identity_association.ebs_csi]
  tags          = { Project = "relaydesk-capstone" }
}

resource "aws_eks_addon" "metrics_server" {
  cluster_name  = aws_eks_cluster.this.name
  addon_name    = "metrics-server"
  addon_version = "v0.9.0-eksbuild.13"
  depends_on    = [aws_eks_node_group.this]
  tags          = { Project = "relaydesk-capstone" }
}
