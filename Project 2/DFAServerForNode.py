# DFAServer, ver. 200127 v6
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST_NAME = '127.0.0.1'
PORT_NUMBER = 1234  # Maybe set this to 1234

# Stores the path to DFAServer working directory
pathToDFA = "C:\\Users\\Marianne Pettersen\\Desktop\\auto\\DFA's"

# Read the content of the template file
f = open(pathToDFA + "\\Templates\\Node_temp.dfa", "r")
data = f.read()

#default values
force = None
torque = None
i = 0
hole_diameter = 0
node_diameter = hole_diameter*4
cutting_radius = node_diameter*0.04

data = data.replace("<PARAM1>", str(node_diameter))
data = data.replace("<PARAM2>", str(hole_diameter))
data = data.replace("<PARAM3>", str(cutting_radius))



f = open(pathToDFA + "\\Node_finished.dfa", "w")
f.write(data)
f.close()


class MyHandler(BaseHTTPRequestHandler): # the class to access the server, render on the site and send input back.

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        global i, hole_diameter, node_diameter, cutting_radius, force, torque
        if os.path.exists("C:\\Users\\Marianne Pettersen\\PycharmProjects\\Automatisering\\Node_project\\resultw.gif"):
            os.remove("C:\\Users\\Marianne Pettersen\\PycharmProjects\\Automatisering\\Node_project\\resultw.gif")
        """Respond to a GET request."""

        s.send_response(200)

        # Check what is the path
        path = s.path
        if path.find(".gif") != -1:
            # Return image file
            s.send_header("Content-type", "image/gif")
            s.end_headers()
            s.wfile.write(open("./result.gif", "rb").read())

        if path.find("/info") != -1:
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write(
                bytes('<html><head><title>Order Site.</title><meta http-equiv="refresh" content="3"></head>',
                      'utf-8'))
            s.wfile.write(bytes("<body><p>Your Order.</p>" + str(i), "utf-8"))
            i = i + 1
            # adding our message
            s.wfile.write(bytes("<p>Force: " + str(force) + "</p>", "utf-8"))
            s.wfile.write(bytes("<p>Torque: " + str(torque) + "</p>", "utf-8"))
            s.wfile.write(bytes("<p>Diameter of hole: " + str(hole_diameter) + "</p>", "utf-8"))
            s.wfile.write(bytes("<p>Diameter of node: " + str(node_diameter) + "</p>", "utf-8"))
            s.wfile.write(bytes("Underneath is a animation of the stress inflicted on the node. <br>", "utf-8"))
            s.wfile.write(bytes("(Maximum stress for Aluminum is 290 MPa)", "utf-8"))
            """
                       rendering the gif
            """
            s.wfile.write(bytes('<br><IMG SRC="result.gif" width="400" height="300">', 'utf-8'))

            s.wfile.write(bytes("</body></html>", "utf-8"))

        if path.find("/productConfig") != -1:
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write(bytes(
                '<html><body><h2>Requirements for the node:</h2><form action="http://127.0.0.1:1234/product" method="post">Force:<br><input type="text" name="force" value="' + str(
                    force), "utf-8"))
            s.wfile.write(bytes('"><br>Torque:<br><input type="text" name="torque" value="' + str(torque), "utf-8"))
            s.wfile.write(
                bytes('"><br>Diameter of hole:<br><input type="text" name="hole_diameter" value="' + str(hole_diameter),
                      "utf-8"))
            s.wfile.write(bytes(
                '"><br><br><input type="submit" value="Submit"></form><p>Click "Submit" to send your requirements.</p></body></html>',
                "utf-8"))


    def do_POST(s): # the method to save the input from the user.
        global i,  force, torque, hole_diameter, cutting_radius, node_diameter

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
                    node_diameter = int(param_line)
                if param_line.find("PARAM2") != -1:
                    param_line = param_line.replace("PARAM2 ", "")
                    hole_diameter = int(param_line)
                if param_line.find("PARAM2") != -1:
                    param_line = param_line.replace("PARAM2 ", "")
                    cutting_radius = int(param_line)

        if path.find("/product") != -1:
            print("Inside of /product path")
            content_len = int(s.headers.get('Content-Length'))
            post_body = s.rfile.read(content_len)

            # process string of parameters:
            # Example: force=1000&torque=2000&hole_diameter=10
            body = post_body.decode()
            print(body)
            pairs = body.split("&")
            # First pair
            pair0 = pairs[0].split("=")
            force = int(pair0[1])
            print("Force is: ", force)
            # Second pair
            pair1 = pairs[1].split("=")
            torque = int(pair1[1])
            print("Torque is: ", torque)
            pair2 = pairs[2].split("=")
            hole_diameter = int(pair2[1])
            print("Hole diameter is: ", hole_diameter)
            # Parameters requested by customer
            node_diameter = hole_diameter * 5
            cutting_radius = node_diameter * 0.04
            print("Node diameter is: ", node_diameter)
            print("Cutting radius is: ", cutting_radius)
            s.updateDesign(node_diameter, hole_diameter, cutting_radius)


    def updateDesign(self, param1, param2, param3):# the method to update the design to the dfa-file.
        # Read the content of the template file
        global pathToDFA
        f = open(pathToDFA + "\\Templates\\Node_temp.dfa", "r")
        data = f.read()
        # data being replaced with the placeholders.
        data = data.replace("<PARAM1>", str(param1))
        data = data.replace("<PARAM2>", str(param2))
        data = data.replace("<PARAM3>", str(param3))
        data = data.replace("Node_temp", "Node_finished")

        print("param1: ", param1)
        print("param2: ", param2)
        print("param3: ", param3)

        f = open(pathToDFA + "\\Node_finished.dfa", "w")
        f.write(data)
        f.close()


if __name__ == '__main__': # main method to start the server.
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

