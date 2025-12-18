pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:

  - name: sonar-scanner
    image: sonarsource/sonar-scanner-cli
    command: ["sh", "-c", "sleep 3600"]
    tty: true

  - name: dind
    image: docker:dind
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""
    command: ["sh", "-c", "dockerd-entrypoint.sh & sleep 3600"]
    volumeMounts:
    - name: docker-config
      mountPath: /etc/docker/daemon.json
      subPath: daemon.json

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ["sh", "-c", "sleep 3600"]
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

  volumes:
  - name: docker-config
    configMap:
      name: docker-daemon-config
  - name: kubeconfig-secret
    secret:
      secretName: kubeconfig-secret
"""
    }
  }

  stages {

    stage('Checkout Code') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        container('dind') {
          sh '''
            docker info
            docker build -t health-tracker:v2 .
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
                -Dsonar.projectKey=2401008_sam \
                -Dsonar.sources=. \
                -Dsonar.host.url=http://my-sonarqube-sonarqube.sonarqube.svc.cluster.local:9000 \
                -Dsonar.token=$SONAR_TOKEN
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
              -u student -p Imcc@2025
          '''
        }
      }
    }

    stage('Push Docker Image') {
      steps {
        container('dind') {
          sh '''
            docker tag health-tracker:v2 \
              nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401008_sam/health-tracker:v2

            docker push \
              nexus-service-for-docker-hosted-registry.nexus.svc.cluster.local:8085/2401008_sam/health-tracker:v2
          '''
        }
      }
    }

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
