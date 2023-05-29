# How to run task
1. Install dependencies:
   1. python
   2. selenium
   3. pytest
2. From the command-line, run `pytest --pdb`.
3. The script should load the webpage and pause. Now:
   1. Log in with username `ryanfrost2015@gmail.com` & password `Helicopter2023!`
   2. Ensure multiple items are in the cart.
   3. Go to the cart page.
   4. Remove any discount code already added.
   5. Click 'Accept' on the cookies pop-up.
4. Resume the debugger by entering `continue`.