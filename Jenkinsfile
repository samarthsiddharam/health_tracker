pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:

  - name: sonar-scanner
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
    securityContext:
      runAsUser: 0
      readOnlyRootFilesystem: false
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
        IMAGE_TAG  = "v2"
        NAMESPACE  = "2401008"
        NEXUS_REGISTRY = "nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085"
        NEXUS_REPO = "2401008_sam"
    }

    stages {

        /* =====================
           Build Docker Image
        ===================== */
        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh '''
                        echo "Waiting for Docker daemon..."
                        sleep 15
                        docker info
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    '''
                }
            }
        }

        /* =====================
           SonarQube Analysis
        ===================== */
        stage('SonarQube Analysis') {
            steps {
                container('sonar-scanner') {
                    withCredentials([
                        string(credentialsId: 'jenkins-token-08', variable: 'SONAR_TOKEN')
                    ]) {
                        sh '''
                            sonar-scanner \
                              -Dsonar.projectKey=2401008_health_tracker \
                              -Dsonar.projectName=Health-Tracker-2401008 \
                              -Dsonar.sources=. \
                              -Dsonar.host.url=http://my-sonarqube-sonarqube.sonarqube.svc.cluster.local:9000 \
                              -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }

        /* =====================
           Login to Nexus
        ===================== */
        stage('Login to Nexus') {
            steps {
                container('dind') {
                    sh '''
                        docker login ${NEXUS_REGISTRY} \
                        -u student -p Imcc@2025
                    '''
                }
            }
        }

        /* =====================
           Tag & Push Image
        ===================== */
        stage('Push Docker Image') {
            steps {
                container('dind') {
                    sh '''
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${NEXUS_REGISTRY}/${NEXUS_REPO}/${IMAGE_NAME}:${IMAGE_TAG}

                        docker push \
                        ${NEXUS_REGISTRY}/${NEXUS_REPO}/${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        /* =====================
           Deploy to Kubernetes
        ===================== */
        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl') {
                    sh '''
                        kubectl create namespace ${NAMESPACE} \
                        --dry-run=client -o yaml | kubectl apply -f -

                        kubectl apply -f deployment.yaml -n ${NAMESPACE}

                        kubectl rollout status deployment/health-tracker-deployment \
                        -n ${NAMESPACE}
                    '''
                }
            }
        }

        /* =====================
           Debug Info (IMPORTANT)
        ===================== */
        stage('Debug Kubernetes State') {
            steps {
                container('kubectl') {
                    sh '''
                        echo "====== PODS ======"
                        kubectl get pods -n ${NAMESPACE}

                        echo "====== SERVICES ======"
                        kubectl get svc -n ${NAMESPACE}

                        echo "====== INGRESS ======"
                        kubectl get ingress -n ${NAMESPACE}

                        echo "====== APP LOGS ======"
                        kubectl logs -l app=health-tracker -n ${NAMESPACE} || true
                    '''
                }
            }
        }
    }
}
