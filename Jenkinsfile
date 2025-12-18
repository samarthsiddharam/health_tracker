pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:

  # Sonar Scanner Container
  - name: sonar-scanner
    image: sonarsource/sonar-scanner-cli
    command: [ "cat" ]
    tty: true

  # Docker-in-Docker Container
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

  # kubectl Container
  - name: kubectl
    image: bitnami/kubectl:latest
    command: [ "cat" ]
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

    stages {

        /* ----------------------
            Checkout
        ---------------------- */
        stage('Checkout Code') {
            steps {
                container('kubectl') {
                    git url: 'https://github.com/samarthsiddharam/health_tracker.git', branch: 'main'
                }
            }
        }

        /* ----------------------
            Build Docker Image
        ---------------------- */
        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh '''
                        sleep 10
                        docker build -t static-site:latest .
                        docker image ls
                    '''
                }
            }
        }

        /* ----------------------
            SonarQube Analysis
        ---------------------- */
        stage('SonarQube Analysis') {
            steps {
                container('sonar-scanner') {
                    withCredentials([string(credentialsId: 'jenkins-token-08', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            sonar-scanner \
                              -Dsonar.projectKey=2401008_sam \
                              -Dsonar.sources=. \
                              -Dsonar.host.url=http://my-sonarqube-sonarqube.sonarqube.svc.cluster.local:9000 \
                              -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }

        /* ----------------------
            Login to Nexus
        ---------------------- */
        stage('Login to Nexus Registry') {
    steps {
        container('dind') {
            sh '''
                docker login nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085 \
                    -u student -p Imcc@2025
            '''
        }
    }
}


        /* ----------------------
            Push Image
        ---------------------- */
       stage('Push Docker Image') {
    steps {
        container('dind') {
            sh '''
                docker tag static-site:latest \
                nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401008_sam/static-site:latest

                docker push \
                nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401008_sam/static-site:latest

                docker pull \
                nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401008_sam/static-site:latest
            '''
        }
    }
}



        /* ----------------------
            Deploy to Kubernetes
        ---------------------- */
        stage('Deploy to Kubernetes') {
    steps {
        container('kubectl') {
            sh '''
                kubectl create namespace 2401008 --dry-run=client -o yaml | kubectl apply -f -
                kubectl apply -f deployment.yaml -n 2401008
            '''
        }
    }
}

    }
}
