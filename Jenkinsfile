pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/gnaanesh-ks/2tier_web_app_using_docker_jenkins.git',
                    branch: 'main'
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }

        stage('Done') {
            steps {
                echo 'App is running on port 5000'
            }
        }
    }

    post {
        failure {
            echo 'Build failed!'
        }
    }
}
