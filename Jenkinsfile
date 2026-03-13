pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'cyborden/bpims-django-api:latest'
        DOCKER_REGISTRY = 'docker.io'
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-cred' // Jenkins credential with kubeconfig
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}