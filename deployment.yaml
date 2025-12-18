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
    command:
    - cat
    tty: true

  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
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

        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh '''
                        sleep 15
                        docker build -t health-tracker:latest .
                        docker image ls
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                container('sonar-scanner') {
                     withCredentials([string(credentialsId: 'jenkins-token-08', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            sonar-scanner \
                                -Dsonar.projectKey=2401008_health_tracker \
                                -Dsonar.projectName=health-tracker-2401008 \
                                -Dsonar.host.url=http://my-sonarqube-sonarqube.sonarqube.svc.cluster.local:9000 \
                                -Dsonar.login=$SONAR_TOKEN \
                                -Dsonar.sources=. 
                        '''
                    }
                }
            }
        }

        stage('Login to Docker Registry') {
            steps {
                container('dind') {
                    sh 'docker --version'
                    sh 'sleep 10'
                    sh 'docker login nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085 -u student -p Imcc@2025'
                }
            }
        }

        stage('Build - Tag - Push') {
            steps {
                container('dind') {
                    sh '''
                        docker tag health-tracker:latest nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401008_sam/health-tracker:latest
                        docker push nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401008_sam/health-tracker:latest
                        docker pull nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401008_sam/health-tracker:latest
                        docker image ls
                    '''
                }
            }
        }
        
        stage('Deploy App') {
            steps {
                container('kubectl') {
                    script {
                        dir('k8s') {
                            sh '''
                                kubectl apply -f deployment.yaml
                                kubectl rollout status deployment/health-tracker-deployment -n 2401008
                            '''
                        }
                    }
                }
            }
        }
    }
}
