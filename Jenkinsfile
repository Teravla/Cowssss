pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'gpu-integration', url: 'https://github.com/Teravla/Cowssss.git'
            }
        }

        stage('Setup Python environment') {
            steps {
                script {
                    bash -c 'python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt'

                }
            }
        }

        stage('Run script') {
            steps {
                script {
                    bash -c '
                    source venv/bin/activate
                    python main.py
                    '
                    
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
