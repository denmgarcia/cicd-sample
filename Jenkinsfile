pipeline {
    agent any

    environment {
        IMAGE_NAME = "cyborden/cicd-sample"  // Replace with your DockerHub repo
        IMAGE_TAG = "${env.GIT_COMMIT.take(7)}"
        SECRET_KEY = credentials('django-secret-key')
        POSTGRES_DB = credentials('POSTGRES_DB')
        POSTGRES_USER = credentials('POSTGRES_USER')
        POSTGRES_PASSWORD = credentials('POSTGRES_PASSWORD')
        POSTGRES_HOST = credentials('POSTGRES_HOST')
        POSTGRES_PORT = credentials('POSTGRES_PORT')
        DJANGO_SETTINGS_MODULE = credentials('DJANGO_SETTINGS_MODULE')
        DEBUG = credentials('DEBUG')
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
                        "--build-arg POSTGRES_DB=${POSTGRES_DB} " +
                        "--build-arg POSTGRES_USER=${POSTGRES_USER} " +
                        "--build-arg POSTGRES_PASSWORD=${POSTGRES_PASSWORD} ."
                    )
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker image to Docker Hub (public)...'
                script {
                    // This 'id' must match the ID you created in Jenkins
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def myImage = docker.image("${IMAGE_NAME}:${IMAGE_TAG}")
                        myImage.push()
                        myImage.push("latest")
            }
                }
            }
        }

        stage('Update Kubernetes Manifests') {
            steps {
                script {

                    def manifestPath = "bpims/kubernetes/deployment.yml"
                    
                    sh """
                        # Replace image tag in deployment.yaml
                        # sed -i "s|cyborden/cicd-sample:.*|cyborden/cicd-sample:${IMAGE_TAG}|g" ${manifestPath}

                        # Commit and push the updated manifest
                        # git config user.email "dengarcia.x@gmail.com"
                        # git config user.name "Jenkins CI"
                        # git add kubernetes/deployment.yaml
                        # git commit -m "Update image tag to ${IMAGE_TAG}"
                        # git push origin main
                        ls -la kubernetes 
                    """
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
