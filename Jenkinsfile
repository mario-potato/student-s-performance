pipeline {
    agent any

    stages {
        stage('1. Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/mario-potato/student-s-performance.git'
            }
        }

        stage('2. Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('3. Deploy Gradio App') {
            steps {
                sh '''
                    . venv/bin/activate
                    # Kill previous app instance if running
                    pkill -f "python3 main.py" || true

                    # Launch Gradio app in background
                    nohup python3 main.py > gradio.log 2>&1 &
                '''
                echo '🚀 Gradio Student Performance App is running on port 7860!'
            }
        }
    }
}
