# DFAServer, ver. 200127 v6
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
HOST_NAME = '127.0.0.1'
PORT_NUMBER = 1234  # Maybe set this to 1234

# Stores the path to DFAServer working directory
pathToApp = "C:\\Users\\Marianne Pettersen\\Desktop\\auto\\DFA's"

# Read the content of the template file
f = open(pathToApp + "\\Templates\\chair_temp.dfa", "r")
data = f.read()
#default values
leg_length = 0
leg_side = 0
seat_length = 0
seat_width = 0
height_backplate = 0
cussion_color = "COLOR"
chair_color = "COLOR"
i = 0
productOK = 0

data = data.replace("<PARAM1>", str(leg_length))
data = data.replace("<PARAM2>", str(leg_side))
data = data.replace("<PARAM3>", str(seat_length))
data = data.replace("<PARAM4>", str(seat_width))
data = data.replace("<PARAM5>", str(height_backplate))


f = open(pathToApp + "\\chair_finished.dfa", "w")
f.write(data)
f.close()


class MyHandler(BaseHTTPRequestHandler): # the class to access the server, render on the site and send input back.

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        global productOK, leg_length, leg_side, seat_length, seat_width, height_backplate, cussion_color, chair_color, i
        """Respond to a GET request."""

        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        # Check what is the path
        path = s.path
        if path.find("/info") != -1:
            s.wfile.write(
                bytes('<html><head><title>Order Site.</title><meta http-equiv="refresh" content="3"></head>',
                      'utf-8'))
            s.wfile.write(bytes("<body><p>Your Order.</p>" + str(i), "utf-8"))
            i = i + 1
            # adding our message
            s.wfile.write(bytes("<p>leg_length: " + str(leg_length) + "</p>", "utf-8"))
            s.wfile.write(bytes("<p>leg_side: " + str(leg_side) + "</p>", "utf-8"))
            s.wfile.write(bytes("<p>seat_length: " + str(seat_length) + "</p>", "utf-8"))
            s.wfile.write(bytes("<p>seat_width: " + str(seat_width) + "</p>", "utf-8"))
            s.wfile.write(bytes("<p>height_backplate: " + str(height_backplate) + "</p>", "utf-8"))

            if productOK:
                s.wfile.write(bytes("<p>Product is possible to make.</p>", "utf-8"))
            else:
                s.wfile.write(bytes("<p>Product is not possible to make.</p>", "utf-8"))
            s.wfile.write(bytes("</body></html>", "utf-8"))
        if path.find("/productConfig") != -1:
            s.wfile.write(bytes(
                '<html><body><h2>Order details:</h2><form action="http://127.0.0.1:1234/product" method="post">Leg length:<br><input type="text" name="leg_length" value="' + str(leg_length), "utf-8"))
            s.wfile.write(
                bytes('"><br>leg_side:<br><input type="text" name="leg_side" value="' + str(leg_side), "utf-8"))
            s.wfile.write(
                bytes('"><br>seat_length:<br><input type="text" name="seat_length" value="' + str(seat_length), "utf-8"))
            s.wfile.write(
                bytes('"><br>seat_width:<br><input type="text" name="seat_width" value="' + str(seat_width), "utf-8"))
            s.wfile.write(
                bytes('"><br>height_backplate:<br><input type="text" name="height_backplate" value="' + str(height_backplate), "utf-8"))

            s.wfile.write(
                bytes('"><br>Color of cussion:<br><select name="cussion_color"><option value="LIGHT_DULL_CYAN">Light Cyan</option><option value="OBSCURE_DULL_MAGENTA">Medium Magenta</option><option value="OBSCURE_DULL_TEAL">Dark Green</option><option value="OBSCURE_DULL_RED">Dark Red</option></optgroup></select>', "ascii"))

            s.wfile.write(
                bytes('<br>Color of chair:<br><select name="chair_color"><option value="OBSCURE_DULL_CYAN">Dark Cyan</option><option value="OBSCURE_WEAK_MAGENTA">Dark Magenta</option><option value="OBSCURE_DULL_RED">Dark Red</option><option value="BLACK">Black</option></optgroup></select>', "ascii"))

            s.wfile.write(bytes(
                '<br><br><input type="submit" value="Submit"></form><p>If you click the "Submit" button, your order will be sent.</p></body></html>',
                "utf-8"))

    def do_POST(s): # the method to save the input from the user.
        global leg_length, leg_side, seat_length, seat_width, height_backplate, cussion_color, chair_color, i, productOK

        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        path = s.path
        print("Path: ", path)
        if path.find("/"):
            content_len = int(s.headers.get('Content-Length'))
            post_body = s.rfile.read(content_len)
            print("Body: ", post_body.decode())
            # Extract params values
            param_line = post_body.decode()
            if param_line.find("PARAM") != -1:
                if param_line.find("PARAM1") != -1:
                    param_line = param_line.replace("PARAM1 ", "")
                    leg_length = int(param_line)
                if param_line.find("PARAM2") != -1:
                    param_line = param_line.replace("PARAM2 ", "")
                    leg_side = int(param_line)
                if param_line.find("PARAM3") != -1:
                    param_line = param_line.replace("PARAM3 ", "")
                    seat_length = int(param_line)
                if param_line.find("PARAM4") != -1:
                    param_line = param_line.replace("PARAM4 ", "")
                    seat_width = int(param_line)
                if param_line.find("PARAM5") != -1:
                    param_line = param_line.replace("PARAM5 ", "")
                    height_backplate = int(param_line)
                if param_line.find("PARAM6") != -1:
                    param_line = param_line.replace("PARAM6 ", "")
                    chair_color = int(param_line)
                if param_line.find("PARAM7") != -1:
                    param_line = param_line.replace("PARAM7 ", "")
                    cussion_color = int(param_line)

        if path.find("/product") != -1:
            print("Inside of /product path")
            content_len = int(s.headers.get('Content-Length'))
            post_body = s.rfile.read(content_len)

            # process string of parameters:
            # Example: leg_length=70&leg_side=5&seat_length=50&seat_width=60&height_backplate=70&cussion_color=OBSCURE_DULL_TEAL&chair_color=BLACK
            body = post_body.decode()
            print(body)
            pairs = body.split("&")
            # First pair
            pair0 = pairs[0].split("=")
            leg_length = int(pair0[1])
            print("leg length is: ", leg_length)
            # Second pair
            pair1 = pairs[1].split("=")
            leg_side = int(pair1[1])
            print("leg side is: ", leg_side)
            # Third pair
            pair2 = pairs[2].split("=")
            seat_length = int(pair2[1])
            print("seat length is: ", seat_length)
            # Fourth pair
            pair3 = pairs[3].split("=")
            seat_width = int(pair3[1])
            print("seat width is: ", seat_width)
            # Fifth pair
            pair4 = pairs[4].split("=")
            height_backplate = int(pair4[1])
            print("height backplate is: ", height_backplate)
            pair5 = pairs[5].split("=")
            cussion_color = str(pair5[1])
            print("cussion color is: ", cussion_color)
            pair6 = pairs[6].split("=")
            chair_color = str(pair6[1])
            print("chair color is: ", chair_color)


            # Parameters requested by customer
            s.updateDesign(leg_length, leg_side, seat_length, seat_width, height_backplate, cussion_color, chair_color)

            # Calls for manuf. constraints (10 constraints in our case). See if the product can be made.
            productOK = 1

            s.getConstrain("leg_length_max", "<PARAM1max>")
            s.getConstrain("leg_length_min", "<PARAM1min>")
            s.getConstrain("leg_side_max", "<PARAM2max>")
            s.getConstrain("leg_side_min", "<PARAM2min>")
            s.getConstrain("seat_length_max", "<PARAM3max>")
            s.getConstrain("seat_length_min", "<PARAM3min>")
            s.getConstrain("seat_width_max", "<PARAM4max>")
            s.getConstrain("seat_width_min", "<PARAM4min>")
            s.getConstrain("height_backplate_max", "<PARAM5max>")
            s.getConstrain("height_backplate_min", "<PARAM5min>")

    def updateDesign(self, param1, param2, param3, param4, param5, param6, param7):# the method to update the design to the dfa-file.
        # Read the content of the template file
        global pathToApp
        f = open(pathToApp + "\\Templates\\chair_temp.dfa", "r")
        data = f.read()
        # data being replaced with the placeholders.
        data = data.replace("<PARAM1>", str(param1))
        data = data.replace("<PARAM2>", str(param2))
        data = data.replace("<PARAM3>", str(param3))
        data = data.replace("<PARAM4>", str(param4))
        data = data.replace("<PARAM5>", str(param5))
        data = data.replace("<PARAM6>", str(param6))
        data = data.replace("<PARAM7>", str(param7))
        data = data.replace("chair_temp", "chair_finished")


        f = open(pathToApp + "\\chair_finished.dfa", "w")
        f.write(data)
        f.close()

    def getConstrain(self, constrain, paramTag): # the method that gets the max-min boundaries from the fuseki-server, and checks them against the input from the user
        global leg_length, leg_side, seat_length, seat_width, height_backplate, productOK
        URL = "http://127.0.0.1:3030/kbe/query"

        # making a query for recieving data from fuseki-server
        PARAMS = {
            'query': 'PREFIX kbe:<http://kbe.openode.io/table-kbe.owl#> SELECT ?data WHERE {?inst kbe:' + constrain + ' ?data.}'}

        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()

        # Checking the value of the parameter
        print("Data:", data['results']['bindings'][0]['data']['value'])

        # Update constrain value in design template
        dataToWrite = data['results']['bindings'][0]['data']['value']
        f = open(pathToApp + "\\Templates\\chair_temp.dfa", "r")
        data = f.read()

        f.close()

        # Check for validity:
        if paramTag.find("1min") != -1:
            if leg_length < int(dataToWrite):
                productOK = 0
        elif paramTag.find("1max") != -1:
            if leg_length > int(dataToWrite):
                productOK = 0
        elif paramTag.find("2min") != -1:
            if leg_side < int(dataToWrite):
                productOK = 0
        elif paramTag.find("2max") != -1:
            if leg_side > int(dataToWrite):
                productOK = 0
        elif paramTag.find("3min") != -1:
            if seat_length < int(dataToWrite):
                productOK = 0
        elif paramTag.find("3max") != -1:
            if seat_length > int(dataToWrite):
                productOK = 0
        elif paramTag.find("4min") != -1:
            if seat_width < int(dataToWrite):
                productOK = 0
        elif paramTag.find("4max") != -1:
            if seat_width > int(dataToWrite):
                productOK = 0
        elif paramTag.find("5min") != -1:
            if height_backplate < int(dataToWrite):
                productOK = 0
        elif paramTag.find("5max") != -1:
            if height_backplate > int(dataToWrite):
                productOK = 0


if __name__ == '__main__': # main method to start the server.
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
