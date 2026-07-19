from sqlalchemy import Column, Integer, String, TIMESTAMP, Date, ForeignKey, text
from sqlalchemy.orm import relationship
from .database import Base


class Income_tab(Base):
    __tablename__ = "income_transactions"

    id = Column(Integer, primary_key=True, index=True)

    # User who owns this transaction
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    amnt = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    owner = relationship("user", back_populates="transactions")


class user(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    transactions = relationship("Income_tab", back_populates="owner")