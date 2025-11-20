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
