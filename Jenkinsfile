pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Cloner le repository contenant main.py
                git 'https://github.com/Teravla/Cowssss.git'
            }
        }

        stage('Setup Environment') {
            steps {
                // Installer les dépendances si nécessaire
                sh 'python -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run main.py') {
            steps {
                // Exécuter le script Python
                sh 'source venv/bin/activate && python main.py'
            }
        }
    }

    post {
        always {
            // Archive les fichiers de build, résultats de tests, etc.
            archiveArtifacts artifacts: '**/target/*.*', allowEmptyArchive: true

            // Nettoyer l'environnement de build
            cleanWs()
        }
    }
}
