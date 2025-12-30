pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

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
