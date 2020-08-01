import openai
import json

settings = json.loads(open('settings.json').read())
openai.api_key = settings['gpt3_api_key']


# This method uses GPT-3 to generate LaTeX from a plain text description using few-shot learning
def generate(textIn):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=r'''Q: A 2x2 matrix containing 2, 3, 4, 5.
            A: \begin{bmatrix} 2 & 3 \\ 4 & 5 \end{bmatrix}
    
            Q: A vector in R^3 containing 5, 6, 7.
            A: \langle 5, 6, 7 \rangle
    
            Q: The partial derivative of f(x,y) with respect to x.
            A: \frac{\partial f}{\partial x}
    
            Q: The determinant of a 2x2 matrix containing ones.
            A: \det \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}
    
            Q: The absolute value of f(x,y) - L is less than epsilon.
            A: \|f(x,y) - L\| < \epsilon
            
            Q: Theta equals (arccos( -4 over 3 root 26))
            A: \theta = \arccos(\frac{-4}{3\sqrt{26}})
    
            Q: ''' + textIn,
            max_tokens=100,
            stop=["Q:"],  # Stop generating when it tries to repeat the pattern
            temperature=0
        )
        text = getattr(getattr(response, "choices")[0], "text")  # Retrieving the generated response
        textOut = text[text.find("A:") + 3:]
        print(textOut)
        return textOut

    except openai.error.APIError as e:
        print(repr(e))
        print("Failed: GPT-3 server is overloaded, try again later")
