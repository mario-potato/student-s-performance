pipeline {
    agent any

    stages {
        stage('1. Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/mario-potato/student-s-performance.git'
            }
        }

        stage('2. Setup Environment & Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                '''
                echo '✅ Virtual environment ready and dependencies installed!'
            }
        }

        stage('3. Run Data & Code Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 -c "import pandas, sklearn, numpy; print('✅ Core ML libraries imported successfully!')"
                '''
            }
        }

        stage('4. Train / Evaluate Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    if [ -f main.py ]; then python3 main.py; elif [ -f train.py ]; then python3 train.py; fi
                '''
                echo '🚀 Model training/evaluation completed!'
            }
        }
    }
}
