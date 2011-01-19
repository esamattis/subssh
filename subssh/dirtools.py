
import os


def create_required_directories_or_die(directories):
    """
    Try to create directories in given order. Raises SystemExit if creation fails 
    """
    for dir in directories:
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except OSError, e:
                sys.stderr.write("Cannot create dir '%s' Reason: %s \n"
                                 % (dir, " ".join(e.args()) ))
                sys.exit(1)

