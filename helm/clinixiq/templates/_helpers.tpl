{{/* Expand the name of the chart. */}}
{{- define "clinixiq.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Common labels */}}
{{- define "clinixiq.labels" -}}
helm.sh/chart: {{ include "clinixiq.name" . }}-{{ .Chart.Version | replace "+" "_" }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: clinixiq-platform
{{- end }}
