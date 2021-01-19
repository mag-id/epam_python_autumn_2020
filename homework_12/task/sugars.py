"""
Functions for comfortable setups and
interaction with sqlalchemy sessions.
"""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__all__ = ["session_manager", "setup_session"]

Session = sessionmaker()


# https://youtu.be/36yw8VC3KU8?t=785
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html
@contextmanager
def session_manager(
    url: str,
    declarative_meta: "DeclarativeMeta",
    echo: bool = False,
) -> Session:
    """
    Takes `url` with `declarative_meta` and setup `Session`.

    Context manager yields `Session` instance and guarantees
    it's committing and closing.

    By default `echo` is `False` (Set `True` for logging).
    """
    setup_session(url, declarative_meta, echo)
    current = Session()
    try:
        yield current
        current.commit()  # pylint: disable=no-member
    except:
        current.rollback()  # pylint: disable=no-member
        raise
    finally:
        current.close()  # pylint: disable=no-member


def setup_session(url: str, declarative_meta: "DeclarativeMeta", echo: bool = False):
    """
    Takes `url` with `declarative_meta` and setup `Session`.
    By default `echo` is `False` (Set `True` for logging).
    """
    engine = create_engine(url, echo=echo)
    declarative_meta.metadata.create_all(engine)
    Session.configure(bind=engine)
