pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'
    DOCKER_IMAGE = "your-dockerhub-username/movie-ticketing"
    KUBECONFIG_CREDENTIAL = 'kubeconfig-credentials-id'
    K8S_NAMESPACE = 'default'
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install & Test') {
      steps {
        sh 'npm ci'
        // simple test placeholder - add real tests as needed
        sh 'node -e "console.log(\'quick smoke\')"'
      }
    }
    stage('Build Docker Image') {
      steps {
        script {
          sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ."
        }
      }
    }
    stage('Push Image') {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
            sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
            sh "docker tag ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
            sh "docker push ${DOCKER_IMAGE}:latest"
          }
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        script {
          // use configured kubeconfig from credentials (store kubeconfig text as secret file)
          withCredentials([file(credentialsId: env.KUBECONFIG_CREDENTIAL, variable: 'KUBECONFIG_FILE')]) {
            sh 'mkdir -p ~/.kube && cp $KUBECONFIG_FILE ~/.kube/config && chmod 600 ~/.kube/config'
            // update image in deployment manifest and apply
            sh """
              kubectl set image deployment/movie-ticketing movie-ticketing=${DOCKER_IMAGE}:${env.BUILD_NUMBER} --namespace=${K8S_NAMESPACE} || true
              kubectl apply -f kubernetes/service.yaml --namespace=${K8S_NAMESPACE}
              kubectl apply -f kubernetes/deployment.yaml --namespace=${K8S_NAMESPACE}
              kubectl apply -f kubernetes/hpa.yaml --namespace=${K8S_NAMESPACE} || true
            """
          }
        }
      }
    }
  }
  post {
    failure { mail to: 'dev-team@example.com', subject: "Pipeline failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}", body: "See Jenkins." }
  }
}
