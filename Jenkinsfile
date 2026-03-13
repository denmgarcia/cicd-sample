pipeline {
    agent any

    environment {
        IMAGE_NAME = "cyborden/cicd-sample"  // Replace with your DockerHub repo
        IMAGE_TAG = "${env.GIT_COMMIT.take(7)}"
        SECRET_KEY = credentials('django-secret-key')
        POSTGRES_DB = credentials('POSTGRES_DB')
        POSTGRES_USER = credentials('POSTGRES_USER')
        POSTGRES_PASSWORD = credentials('POSTGRES_PASSWORD')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                git branch: 'main', url: 'https://github.com/denmgarcia/cicd-sample.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    // Using your snippet with the environment variables defined above
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}",
                        "--build-arg SECRET_KEY=${SECRET_KEY} " +
                        "--build-arg POSTGRES_DB=${DB_NAME} " +
                        "--build-arg POSTGRES_USER=${DB_USER} " +
                        "--build-arg POSTGRES_PASSWORD=${DB_PASS} ."
                    )
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker image to Docker Hub (public)...'
                script {
                    // No username/password, assumes public repo
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
