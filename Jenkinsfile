pipeline {
    agent any

    stages {
        stage('Check pip installation') {
            steps {
                script {
                    // Vérifier si pip est installé en utilisant la commande pip --version
                    def pipOutput = sh(returnStdout: true, script: 'pip --version')
                    if (pipOutput.contains('not found')) {
                        echo "pip n'est pas installé, installation en cours..."
                        sh 'apt update && apt install -y python3-pip'
                    } else {
                        echo "pip est déjà installé : ${pipOutput}"
                    }

                    // Créer et activer l'environnement virtuel
                    sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    python3 -m pip install --upgrade pip setuptools
                    python3 -m pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run script') {
            steps {
                script {
                    // Utiliser python3 de l'environnement virtuel pour exécuter main.py
                    sh '''
                    source venv/bin/activate
                    python3 main.py
                    '''
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
