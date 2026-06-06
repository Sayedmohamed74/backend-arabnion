from typing import Optional
import datetime

from sqlalchemy import (
    ARRAY,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = "admin"
    __table_args__ = (PrimaryKeyConstraint("id", name="admin_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)


class Package(Base):
    __tablename__ = "package"
    __table_args__ = (PrimaryKeyConstraint("id", name="package_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    lesson: Mapped[str] = mapped_column(String(150), nullable=False)
    mount_paid: Mapped[str] = mapped_column(String(50), nullable=False)
    features: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False)

    student: Mapped[list["Student"]] = relationship("Student", back_populates="package")


class Teacher(Base):
    __tablename__ = "teacher"
    __table_args__ = (PrimaryKeyConstraint("id", name="teacher_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    tel: Mapped[str] = mapped_column(String(50), nullable=False)
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    student: Mapped[list["Student"]] = relationship("Student", back_populates="teacher")


class Student(Base):
    __tablename__ = "student"
    __table_args__ = (
        ForeignKeyConstraint(["package_id"], ["package.id"], name="package_id"),
        ForeignKeyConstraint(
            ["teacher_id"], ["teacher.id"], ondelete="SET NULL", name="teacher_id"
        ),
        PrimaryKeyConstraint("id", name="student_pkey"),
        Index("fki_package_id", "package_id"),
        Index("fki_teacher_id", "teacher_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    tel: Mapped[str] = mapped_column(String(50), nullable=False)
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    teacher_id: Mapped[Optional[int]] = mapped_column(Integer)
    package_id: Mapped[Optional[int]] = mapped_column(Integer)

    package: Mapped[Optional["Package"]] = relationship(
        "Package", back_populates="student"
    )
    teacher: Mapped[Optional["Teacher"]] = relationship(
        "Teacher", back_populates="student"
    )
