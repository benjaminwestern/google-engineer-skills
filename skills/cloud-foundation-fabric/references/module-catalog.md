---
name: cff-module-catalog
version: "1.0.0"
description: Complete catalog of Cloud Foundation Fabric modules organized by category including resource management, networking, load balancers, security, compute, and more.
metadata:
  source_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric
  docs_url: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules
---

# Module Catalog

Complete catalog of Cloud Foundation Fabric modules organized by category.

**[Back to Main Documentation](../SKILL.md)**

---

## Resource Management

| Module | Description | README |
|--------|-------------|--------|
| **project** | Create and manage GCP projects with IAM, APIs, org policies, logging, budgets | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/project) |
| **project-factory** | Factory pattern for creating multiple projects from YAML configuration | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/project-factory) |
| **folder** | Manage GCP folders with IAM, org policies, PAM entitlements, SCC configs | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/folder) |
| **organization** | Manage organization-level IAM, org policies, custom roles, tags | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/organization) |
| **billing-account** | Manage billing accounts and budgets | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/billing-account) |

## Networking

| Module | Description | README |
|--------|-------------|--------|
| **net-vpc** | Create VPC networks with subnets, IAM, firewall rules, VPC Flow Logs | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-vpc) |
| **net-vpc-factory** | Factory pattern for creating multiple VPCs from YAML | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-vpc-factory) |
| **net-vpc-peering** | VPC network peering configuration | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-vpc-peering) |
| **net-vpc-firewall** | Firewall rules management for VPCs | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-vpc-firewall) |
| **net-cloudnat** | Cloud NAT gateway configuration | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-cloudnat) |
| **net-address** | Reserve static IP addresses (internal/external) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-address) |
| **net-vlan-attachment** | VLAN attachments for Dedicated Interconnect | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-vlan-attachment) |

## Load Balancers

| Module | Description | README |
|--------|-------------|--------|
| **net-lb-app-ext** | External Application Load Balancer (Global) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-lb-app-ext) |
| **net-lb-app-ext-regional** | Regional External Application Load Balancer | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-lb-app-ext-regional) |
| **net-lb-app-int** | Internal Application Load Balancer | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-lb-app-int) |
| **net-lb-app-int-cross-region** | Cross-region Internal Application Load Balancer | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-lb-app-int-cross-region) |
| **net-lb-ext** | External Network Load Balancer | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-lb-ext) |
| **net-lb-int** | Internal Network Load Balancer | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-lb-int) |
| **net-lb-proxy-int** | Internal Proxy Network Load Balancer | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-lb-proxy-int) |

## Security & VPC Service Controls

| Module | Description | README |
|--------|-------------|--------|
| **vpc-sc** | VPC Service Controls - Access Policy, Perimeters, Access Levels | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/vpc-sc) |
| **net-firewall-policy** | Hierarchical and VPC firewall policies | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-firewall-policy) |
| **net-swp** | Secure Web Proxy | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-swp) |
| **certificate-manager** | Certificate Manager for TLS certificates | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/certificate-manager) |
| **certificate-authority-service** | Private Certificate Authority | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/certificate-authority-service) |
| **binauthz** | Binary Authorization policies | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/binauthz) |
| **kms** | Cloud KMS key rings and keys | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/kms) |
| **secret-manager** | Secret Manager secrets and versions | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/secret-manager) |
| **secops-rules** | Security Operations (SecOps) rules and reference lists | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/secops-rules) |

## Compute

| Module | Description | README |
|--------|-------------|--------|
| **compute-vm** | Compute Engine VMs with disks, IAM, metadata | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/compute-vm) |
| **compute-mig** | Managed Instance Groups with autoscaling | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/compute-mig) |
| **cloud-run-v2** | Cloud Run services and jobs | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/cloud-run-v2) |
| **cloud-function-v1** | Cloud Functions (1st gen) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/cloud-function-v1) |
| **cloud-function-v2** | Cloud Functions (2nd gen) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/cloud-function-v2) |
| **agent-engine** | Vertex AI Agent Engine (formerly Agent Builder) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/agent-engine) |

## GKE (Google Kubernetes Engine)

| Module | Description | README |
|--------|-------------|--------|
| **gke-cluster-autopilot** | GKE Autopilot clusters | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/gke-cluster-autopilot) |
| **gke-cluster-standard** | GKE Standard clusters | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/gke-cluster-standard) |
| **gke-nodepool** | GKE node pools | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/gke-nodepool) |
| **gke-hub** | GKE Hub and Fleet management | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/gke-hub) |
| **cloud-config-container** | Container configuration for VMs | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/cloud-config-container) |

## Storage & Databases

| Module | Description | README |
|--------|-------------|--------|
| **gcs** | Cloud Storage buckets with IAM, lifecycle, retention | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/gcs) |
| **cloudsql-instance** | Cloud SQL instances (MySQL, PostgreSQL, SQL Server) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/cloudsql-instance) |
| **bigquery-dataset** | BigQuery datasets with IAM, tables, views | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/bigquery-dataset) |
| **bigtable-instance** | Cloud Bigtable instances | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/bigtable-instance) |
| **spanner-instance** | Cloud Spanner instances | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/spanner-instance) |
| **firestore** | Firestore databases | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/firestore) |
| **alloydb** | AlloyDB clusters | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/alloydb) |
| **biglake-catalog** | BigLake catalogs | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/biglake-catalog) |

## Data & Analytics

| Module | Description | README |
|--------|-------------|--------|
| **bigquery-connection** | BigQuery connections (Cloud SQL, Spark, etc.) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/bigquery-connection) |
| **dataproc** | Dataproc clusters | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/dataproc) |
| **datafusion** | Cloud Data Fusion instances | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/datafusion) |
| **dataplex** | Dataplex lakes, zones, and assets | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/dataplex) |
| **dataplex-datascan** | Dataplex data quality scans | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/dataplex-datascan) |
| **dataplex-aspect-types** | Dataplex aspect types | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/dataplex-aspect-types) |
| **analytics-hub** | Analytics Hub exchanges and listings | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/analytics-hub) |
| **dataform-repository** | Dataform repositories | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/dataform-repository) |
| **pubsub** | Pub/Sub topics and subscriptions | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/pubsub) |
| **managed-kafka** | Managed Kafka clusters | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/managed-kafka) |

## Data Governance

| Module | Description | README |
|--------|-------------|--------|
| **data-catalog-policy-tag** | Data Catalog policy tags and taxonomies | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/data-catalog-policy-tag) |
| **data-catalog-tag-template** | Data Catalog tag templates | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/data-catalog-tag-template) |
| **data-catalog-tag** | Data Catalog tags | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/data-catalog-tag) |

## Identity & Access

| Module | Description | README |
|--------|-------------|--------|
| **iam-service-account** | Service accounts with IAM and key management | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/iam-service-account) |
| **cloud-identity-group** | Cloud Identity groups | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/cloud-identity-group) |

## DevOps & CI/CD

| Module | Description | README |
|--------|-------------|--------|
| **artifact-registry** | Artifact Registry repositories | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/artifact-registry) |
| **container-registry** | Container Registry (deprecated, use artifact-registry) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/container-registry) |
| **cloud-build-v2-connection** | Cloud Build connections (GitHub, GitLab, etc.) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/cloud-build-v2-connection) |
| **cloud-deploy** | Cloud Deploy delivery pipelines and targets | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/cloud-deploy) |
| **source-repository** | Cloud Source Repositories | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/source-repository) |
| **secure-source-manager-instance** | Secure Source Manager instances | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/secure-source-manager-instance) |
| **service-directory** | Service Directory namespaces and services | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/service-directory) |
| **endpoints** | Cloud Endpoints | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/endpoints) |
| **api-gateway** | API Gateway configuration | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/api-gateway) |
| **apigee** | Apigee X organization and environments | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/apigee) |

## Monitoring & Logging

| Module | Description | README |
|--------|-------------|--------|
| **logging-bucket** | Cloud Logging buckets | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/logging-bucket) |
| **dns** | Cloud DNS managed zones and record sets | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/dns) |
| **dns-response-policy** | DNS response policies and rules | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/dns-response-policy) |

## Specialized

| Module | Description | README |
|--------|-------------|--------|
| **looker-core** | Looker (Google Cloud Core) instances | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/looker-core) |
| **backup-dr** | Backup and DR service | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/backup-dr) |
| **gcve-private-cloud** | Google Cloud VMware Engine private clouds | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/gcve-private-cloud) |
| **ai-applications** | AI applications (Vertex AI) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/ai-applications) |
| **ncc-spoke-ra** | Network Connectivity Center spoke resources | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/ncc-spoke-ra) |
| **net-ipsec-over-interconnect** | IPSec over Interconnect | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-ipsec-over-interconnect) |
| **net-vpn-ha** | HA VPN gateways and tunnels | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-vpn-ha) |
| **net-vpn-static** | Static VPN tunnels | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-vpn-static) |
| **net-vpn-dynamic** | Dynamic VPN tunnels (BGP) | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-vpn-dynamic) |
| **workstation-cluster** | Cloud Workstations clusters and configurations | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/workstation-cluster) |
| **projects-data-source** | Data source for retrieving project information | [README](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/projects-data-source) |
