from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, Date, ForeignKey, text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    dob = Column(Date, nullable=False)
    password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    transactions = relationship(
        "Transaction", back_populates="owner", cascade="all, delete-orphan"
    )


class Transaction(Base):
    """Stores both income and expense rows; transaction_type distinguishes them."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False)
    # Numeric, not Integer/Float: money needs exact decimal precision.
    amnt = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(String, nullable=False)  # "income" | "expense"
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    owner = relationship("User", back_populates="transactions")
