from flask import Flask, render_template, request, jsonify
from query_processor import QueryProcessor
import json

app = Flask(__name__)
processor = QueryProcessor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        question = request.json.get('question', '')

        if not question:
            return jsonify({'error': 'No question provided'})

        # Process the question
        result = processor.process_query(question)

        return jsonify({
            'answer': result['answer'],
            'sources': result['sources'],
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': f'Error processing question: {str(e)}',
            'success': False
        })


if __name__ == '__main__':
    app.run(debug=True, port=5000)