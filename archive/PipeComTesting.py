import unittest
from PipeCom import SubprocessRunner, PipeHandler, threading

class TestCommunication(unittest.TestCase):
    def test_communication(self):
        # Path to the script and pipe
        script_path = "path/to/executePipeProcess.bat"  # Replace with actual path
        pipe_path = "my_pipe"  # Replace with actual pipe path

        # Initialize SubprocessRunner and PipeHandler objects
        subprocess_runner = SubprocessRunner(script_path)
        pipe_handler = PipeHandler(pipe_path)

        # Start the subprocess in a separate thread
        thread = threading.Thread(target=subprocess_runner.run_script)
        thread.start()

        try:
            # Create the named pipe
            pipe_handler.create_pipe()

            # Message to send
            message = "Hello from Python!"

            # Write message to the pipe
            pipe_handler.write_to_pipe(message)

            # Read response from the pipe
            response = pipe_handler.read_from_pipe()

            # Check if the response matches the expected message
            self.assertEqual(response, "Data from C", "Received response doesn't match expected message")

        except Exception as e:
            # Print any errors that occur
            print(f"An error occurred: {e}")
            self.fail(f"An error occurred: {e}")

        finally:
            # Close the pipe
            pipe_handler.close_pipe()

if __name__ == '__main__':
    unittest.main()
