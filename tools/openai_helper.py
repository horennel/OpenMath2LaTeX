from openai import OpenAI


class OpenAIHelper(object):
    def __init__(self, base_url, api_key, model):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def chat(self, img):
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a math formula converter. Return only the LaTeX formula wrapped in `$$...$$`"
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": 'Convert the math formula in the image to LaTeX'},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpg;base64,{img}"
                                },
                            },
                        ],
                    }
                ]
            )
            return None, resp.choices[0].message.content
        except Exception as e:
            return e, str(e)
