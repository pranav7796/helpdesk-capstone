variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
variable "name" {
  type    = string
  default = "relaydesk-capstone"
}
variable "cluster_version" {
  type    = string
  default = "1.35"
}
variable "vpc_cidr" {
  type    = string
  default = "10.42.0.0/16"
}
variable "cluster_admin_cidr" {
  description = "The single IPv4 address range allowed to reach the EKS public Kubernetes API. Set this to your public IP followed by /32."
  type        = string
  validation {
    condition     = can(cidrnetmask(var.cluster_admin_cidr)) && endswith(var.cluster_admin_cidr, "/32")
    error_message = "Use your trusted public IPv4 address with a /32 prefix."
  }
}
variable "node_instance_types" {
  type    = list(string)
  default = ["t3.medium"]
}
variable "node_desired_size" {
  type    = number
  default = 2
}
variable "node_min_size" {
  type    = number
  default = 2
}
variable "node_max_size" {
  type    = number
  default = 2
}
