from stegano import lsb

def hide_message(image_path, secret_message, output_path):
    
    secret = lsb.hide(image_path, secret_message)
    secret.save(output_path)

def reveal_message(image_path):
    return lsb.reveal(image_path)