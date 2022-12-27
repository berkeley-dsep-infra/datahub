{{/*
Expand the name of the chart.
*/}}
{{- define "node-placeholder-scaler.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "node-placeholder-scaler.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "node-placeholder-scaler.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "node-placeholder-scaler.labels" -}}
helm.sh/chart: {{ include "node-placeholder-scaler.chart" . }}
{{ include "node-placeholder-scaler.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "node-placeholder-scaler.selectorLabels" -}}
app.kubernetes.io/name: {{ include "node-placeholder-scaler.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "node-placeholder-scaler.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "node-placeholder-scaler.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the priority class to use
*/}}
{{- define "node-placeholder-scaler.priorityClassName" -}}
{{- if .Values.priorityClass.create }}
{{- default (include "node-placeholder-scaler.fullname" .) .Values.priorityClass.name }}
{{- else }}
{{- default "default" .Values.priorityClass.name }}
{{- end }}
{{- end }}


{{- define "node-placeholder-scaler.placeholderTemplate" -}}
apiVersion: apps/v1
kind: Deployment
metadata:
    labels:
        app: {{ .Chart.Name }}
        component: placeholder
spec:
    strategy:
        type: Recreate
    selector:
        matchLabels:
            app: {{ .Chart.Name }}
            component: placeholder
    template:
        metadata:
            labels:
                app: {{ .Chart.Name }}
                component: placeholder
        spec:
            priorityClassName: {{ include "node-placeholder-scaler.priorityClassName" . }}
            terminationGracePeriodSeconds: 0
            automountServiceAccountToken: false
            containers:
            - name: pause
              image: k8s.gcr.io/pause:3.2
            tolerations:
            - effect: NoSchedule
              key: hub.jupyter.org/dedicated
              operator: Equal
              value: user
            - effect: NoSchedule
              key: hub.jupyter.org_dedicated
              operator: Equal
              value: user
{{- end -}}