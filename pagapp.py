from pagapp.create_pagapp import create_pagapp


app = create_pagapp('config.Config', debug=True)

if __name__ == "__main__":
    app.run()
