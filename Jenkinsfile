pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
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

        stage('Build Application') {
            steps {
                sh '''
                echo "Building Flask Application"
                . $VENV/bin/activate
                python -m py_compile main.py
                python -m py_compile forms.py
                python -m py_compile init_db.py
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                echo "Deploy stage (skipped actual deployment)"
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
