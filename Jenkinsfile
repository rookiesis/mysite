pipeline {
    agent any

    environment {
        DOCKER_IMAGE        = "hpark8672/django-app"
        DOCKER_CREDENTIALS  = "dockerhub-login"
        GIT_CREDENTIALS     = "github-token"

        MANIFEST_REPO_URL   = "https://github.com/rookiesis/k8s-manifest.git"
        MANIFEST_REPO_DIR   = "k8s-manifest"
    }

    stages {

        stage('Checkout Django Repo') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest .
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: DOCKER_CREDENTIALS,
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    sh """
                    echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                    docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                    docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Update Manifests Repo') {
            steps {
                dir(MANIFEST_REPO_DIR) {
                    script {
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: '*/main']],
                            userRemoteConfigs: [[
                                url: MANIFEST_REPO_URL,
                                credentialsId: GIT_CREDENTIALS
                            ]]
                        ])
                    }

                    sh """
                    sed -i "s|image: hpark8672/django-app:.*|image: hpark8672/django-app:${BUILD_NUMBER}|" django-app/django-deployment.yml
                    """

                    withCredentials([usernamePassword(
                        credentialsId: GIT_CREDENTIALS,
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )]) {
                        sh """
                        git config user.name "rookiesis"
                        git config user.email "hpark8672@gmail.com"

                        git add django-app/django-deployment.yml || true
                        git commit -m "Update Django image to build ${BUILD_NUMBER}" || true

                        git remote set-url origin https://${GIT_USER}:${GIT_TOKEN}@github.com/rookiesis/k8s-manifest.git
                        git push origin HEAD:main
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            sh "docker image prune -f || true"
        }
    }
}
