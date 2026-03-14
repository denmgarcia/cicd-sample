pipeline {
    agent any

    environment {
        IMAGE_NAME = "cyborden/cicd-sample"
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
                git scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
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
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def myImage = docker.image("${IMAGE_NAME}:${IMAGE_TAG}")
                        myImage.push()

                        if (env.BRANCH_NAME == 'main') {
                            myImage.push("latest")
                        } else {
                            myImage.push("${env.BRANCH_NAME}")
                        }
                    }
                }
            }
        }

        stage('Update Kubernetes Manifests') {
            steps {
                // This helper binds your Jenkins credentials to variables the shell can use
                withCredentials([usernamePassword(credentialsId: 'github-creds',
                                 passwordVariable: 'GIT_PASSWORD',
                                 usernameVariable: 'GIT_USERNAME')]) {
                    script {
                        sh '''
                            TARGET="kubernetes/deployment.yml"

                            sed -i "s|image: cyborden/cicd-sample.*|image: cyborden/cicd-sample:${IMAGE_TAG}|g" "$TARGET"

                            git config user.email "dengarcia.x@gmail.com"
                            git config user.name "Jenkins CI"

                            git add "$TARGET"
                            git commit -m "Update image tag to ${IMAGE_TAG}"

                            # We use the variables GIT_USERNAME and GIT_PASSWORD here
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/denmgarcia/cicd-sample.git $BRANCH_NAME
                        '''
                    }
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
