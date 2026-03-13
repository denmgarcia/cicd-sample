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

                    echo "Current workspace: "
                    echo "Checking for files..."
                    
                    FILE_PATH=$(find . -name "deployment.yml" | head -n 1)
    
                    if [ -z "$FILE_PATH" ]; then
                        echo "ERROR: deployment.yml not found. Listing all files for debug:"
                        find . -maxdepth 3 -not -path '*/.*'
                        exit 1
                    fi
    
                    echo "Found file at: $FILE_PATH"

                    
                    sh """
                        # Replace image tag in deployment.yaml
                        sed -i "s|cyborden/cicd-sample:.*|cyborden/cicd-sample:${IMAGE_TAG}|g" "$FILE_PATH"

                        git config user.email "dengarcia.x@gmail.com"
                        git config user.name "Jenkins CI"
                        git add "$FILE_PATH"
                        
                        if ! git diff --cached --exit-code; then
                            git commit -m "Update image tag to ${IMAGE_TAG}"
                            git push origin main
                        else
                            echo "No changes made (tag might be the same)."
                        fi

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
