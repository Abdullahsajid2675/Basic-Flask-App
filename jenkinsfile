pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/USERNAME/flask-app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv $VENV
                . $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                . $VENV/bin/activate
                pytest
                '''
            }
        }

        stage('Build Application') {
            steps {
                sh '''
                echo "Building Flask Application"
                python -m py_compile app.py
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                echo "Deploying Flask Application"
                # Example deployment
                # gunicorn app:app --daemon
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
