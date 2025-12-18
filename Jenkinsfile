pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: sonar
    image: sonarsource/sonar-scanner-cli
    command: ["cat"]
    tty: true

  - name: dind
    image: docker:dind
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""
    volumeMounts:
    - name: docker-config
      mountPath: /etc/docker/daemon.json
      subPath: daemon.json

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ["cat"]
    tty: true
    env:
    - name: KUBECONFIG
      value: /kube/config
    volumeMounts:
    - name: kubeconfig-secret
      mountPath: /kube/config
      subPath: kubeconfig

  volumes:
  - name: docker-config
    configMap:
      name: docker-daemon-config
  - name: kubeconfig-secret
    secret:
      secretName: kubeconfig-secret
'''
        }
    }

    environment {
        IMAGE_NAME = "health-tracker"
        IMAGE_TAG  = "v3"
        NAMESPACE  = "2401008"
        NEXUS_REGISTRY = "nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085"
        NEXUS_REPO = "2401008_sam"
    }

    stages {

        /* ==================================================
           Build Docker Image
        ================================================== */
        stage('Build') {
            steps {
                container('dind') {
                    sh """
                        sleep 15
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    """
                }
            }
        }

        /* ==================================================
           Push to Nexus
        ================================================== */
        stage('Push Image') {
            steps {
                container('dind') {
                    sh """
                        docker login ${NEXUS_REGISTRY} -u student -p Imcc@2025

                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${NEXUS_REGISTRY}/${NEXUS_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

                        docker push \
                        ${NEXUS_REGISTRY}/${NEXUS_REPO}/${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        /* ==================================================
           Deploy to Kubernetes
        ================================================== */
        stage('Deploy K8s') {
            steps {
                container('kubectl') {
                    sh """
                        kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

                        kubectl apply -f deployment.yaml -n ${NAMESPACE}

                        sleep 5
                        kubectl rollout status deployment/health-tracker-deployment -n ${NAMESPACE}
                    """
                }
            }
        }

        /* ==================================================
           Get Logs
        ================================================== */
        stage('Logs') {
            steps {
                container('kubectl') {
                    sh """
                        kubectl get pods -n ${NAMESPACE}
                        kubectl logs -l app=health-tracker -n ${NAMESPACE} --tail=50 || true
                    """
                }
            }
        }
    }
}
