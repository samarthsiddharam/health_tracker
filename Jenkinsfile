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

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ["cat"]
    tty: true
    securityContext:
      runAsUser: 0
    env:
    - name: KUBECONFIG
      value: /kube/config
    volumeMounts:
    - name: kubeconfig-secret
      mountPath: /kube/config
      subPath: kubeconfig

  - name: dind
    image: docker:dind
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""
    command: ["sh", "-c", "dockerd-entrypoint.sh & sleep infinity"]
    volumeMounts:
    - name: docker-config
      mountPath: /etc/docker/daemon.json
      subPath: daemon.json

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

    stages {

        stage('Wait for Docker') {
            steps {
                container('dind') {
                    sh '''
                        echo "Waiting for Docker daemon..."
                        for i in {1..30}; do
                          docker info && break
                          sleep 2
                        done
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh '''
                        docker build -t loan-app:latest .
                        docker images
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                container('sonar-scanner') {
                    withCredentials([string(credentialsId: 'sonar-token-2401034', variable: 'SONAR_TOKEN')]) {
                        sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=LoanPrediction-2401034-V2 \
                          -Dsonar.projectName=LoanPrediction-2401034-V2 \
                          -Dsonar.host.url=http://my-sonarqube-sonarqube.sonarqube.svc.cluster.local:9000 \
                          -Dsonar.login=$SONAR_TOKEN \
                          -Dsonar.sources=. \
                          -Dsonar.python.version=3.10
                        '''
                    }
                }
            }
        }

        stage('Login to Nexus') {
            steps {
                container('dind') {
                    sh '''
                        docker login nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085 \
                          -u admin -p Changeme@2025
                    '''
                }
            }
        }

        stage('Tag & Push Image') {
            steps {
                container('dind') {
                    sh '''
                        docker tag loan-app:latest \
                          nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401034-project/loan-app-2401034-v2:latest

                        docker push \
                          nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401034-project/loan-app-2401034-v2:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl') {
                    dir('k8s') {
                        sh '''
                        kubectl create namespace 2401034 --dry-run=client -o yaml | kubectl apply -f -
                        kubectl apply -f deployment.yaml -n 2401034

                        kubectl rollout restart deployment loan-app-deployment -n 2401034
                        '''
                    }
                }
            }
        }

        stage('DEBUG – Kubernetes State') {
            steps {
                container('kubectl') {
                    sh '''
                    echo "==== PODS ===="
                    kubectl get pods -n 2401034

                    echo "==== SERVICES ===="
                    kubectl get svc -n 2401034

                    echo "==== INGRESS ===="
                    kubectl get ingress -n 2401034

                    echo "==== POD LOGS ===="
                    kubectl logs -l app=loan-app -n 2401034 --tail=50 || true
                    '''
                }
            }
        }
    }
}
