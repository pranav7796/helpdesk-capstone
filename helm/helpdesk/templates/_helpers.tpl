{{- define "relaydesk.name" -}}{{ .Values.nameOverride | default .Chart.Name }}{{- end -}}
{{- define "relaydesk.labels" -}}
app.kubernetes.io/name: {{ include "relaydesk.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end -}}
