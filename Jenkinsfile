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
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {

                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}",
                        "--build-arg SECRET_KEY='${SECRET_KEY}' " +
                        "--build-arg POSTGRES_DB='${POSTGRES_DB}' " +
                        "--build-arg POSTGRES_USER='${POSTGRES_USER}' " +
                        "--build-arg POSTGRES_PASSWORD='${POSTGRES_PASSWORD}' " +
                        "--build-arg POSTGRES_HOST='${POSTGRES_HOST}' " +
                        "--build-arg POSTGRES_PORT='${POSTGRES_PORT}' ."
                    )
                }
            }
        }

        stage('Deploy to DEV') {
            when { branch 'dev' }
            steps {
                echo 'Deploying to Development Namespace...'
                sh """
                    sed -i "s|image: cyborden/cicd-sample.*|image: cyborden/cicd-sample:${IMAGE_TAG}|g" kubernetes/deployment.yml
                    kubectl apply -f kubernetes/deployment.yml -n dev
                """
            }
        }


        stage('Deploy to Staging') {
            when { branch 'staging' }
            steps {
                echo 'Deploying to Staging Namespace...'
                sh """
                    sed -i "s|image: cyborden/cicd-sample.*|image: cyborden/cicd-sample:${IMAGE_TAG}|g" kubernetes/deployment.yml
                    kubectl apply -f kubernetes/deployment.yml -n dev
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def myImage = docker.image("${IMAGE_NAME}:${IMAGE_TAG}")
                        myImage.push()
                        myImage.push("latest")
                    }
                }
            }
        }

        stage('Deploy to PROD & Update Manifests') {
            when { branch 'main' }
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-creds',
                                 passwordVariable: 'GIT_PASSWORD',
                                 usernameVariable: 'GIT_USERNAME')]) {
                    script {
                        sh '''
                            TARGET="kubernetes/deployment.yml"
                            sed -i "s|image: cyborden/cicd-sample.*|image: cyborden/cicd-sample:${IMAGE_TAG}|g" "$TARGET"

                            kubectl apply -f "$TARGET" -n prod

                            git config user.email "dengarcia.x@gmail.com"
                            git config user.name "denmgarcia"
                            git add "$TARGET"
                            git commit -m "Update image tag to ${IMAGE_TAG} [skip ci]"
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/denmgarcia/cicd-sample.git main
                        '''
                    }
                }
            }
        }
    }

    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed!' }
    }
}