from typing import Optional
import datetime
import uuid

from sqlalchemy import (
    ARRAY,
    ForeignKey,
    Column,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = "admin"
    __table_args__ = (PrimaryKeyConstraint("id", name="admin_pkey"),)

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)


class Countries(Base):
    __tablename__ = "countries"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="countries_pkey"),
        UniqueConstraint("country_code", name="country_cod"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country_name: Mapped[Optional[str]] = mapped_column(Text)
    country_code: Mapped[Optional[str]] = mapped_column(String(2))
    phone_code: Mapped[Optional[str]] = mapped_column(Text)
    continent: Mapped[Optional[str]] = mapped_column(Text)

    student: Mapped[list["Student"]] = relationship(
        "Student", back_populates="countries"
    )


class Dialects(Base):
    __tablename__ = "dialects"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="dialects_pkey"),
        UniqueConstraint("name", name="dialects_name_key"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    teacher: Mapped[list["Teacher"]] = relationship(
        "Teacher", secondary="teacher_dialects", back_populates="dialect"
    )
    student: Mapped[list["Student"]] = relationship("Student", back_populates="dialect")


class Package(Base):
    __tablename__ = "package"
    __table_args__ = (PrimaryKeyConstraint("id", name="package_pkey"),)

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    lesson: Mapped[str] = mapped_column(String(150), nullable=False)
    mount_paid: Mapped[str] = mapped_column(String(50), nullable=False)
    features: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False)

    student: Mapped[list["Student"]] = relationship("Student", back_populates="package")


class Teacher(Base):
    __tablename__ = "teacher"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="teacher_pkey"),
        Index("idx_teacher_id", "email"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    tel: Mapped[str] = mapped_column(String(20), nullable=False)
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    rating: Mapped[Optional[str]] = mapped_column(Text)

    dialect: Mapped[list["Dialects"]] = relationship(
        "Dialects", secondary="teacher_dialects", back_populates="teacher"
    )
    student: Mapped[list["Student"]] = relationship("Student", back_populates="teacher")


class Student(Base):
    __tablename__ = "student"
    __table_args__ = (
        ForeignKeyConstraint(
            ["country"], ["countries.country_code"], name="country_code"
        ),
        ForeignKeyConstraint(
            ["dialect_id"],
            ["dialects.id"],
            ondelete="SET NULL",
            name="fk_student_dialect",
        ),
        ForeignKeyConstraint(
            ["package_id"],
            ["package.id"],
            ondelete="SET NULL",
            name="fk_student_package",
        ),
        ForeignKeyConstraint(
            ["teacher_id"],
            ["teacher.id"],
            ondelete="SET NULL",
            name="fk_student_teacher",
        ),
        PrimaryKeyConstraint("id", name="student_pkey"),
        Index("idx_student_id", "email"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    country: Mapped[str] = mapped_column(String(10), nullable=False)
    tel: Mapped[str] = mapped_column(String(20), nullable=False)
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    teacher_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    package_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    dialect_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    rating: Mapped[Optional[str]] = mapped_column(Text)
    group_whatsapp: Mapped[Optional[str]] = mapped_column(Text)

    countries: Mapped["Countries"] = relationship("Countries", back_populates="student")
    dialect: Mapped[Optional["Dialects"]] = relationship(
        "Dialects", back_populates="student"
    )
    package: Mapped[Optional["Package"]] = relationship(
        "Package", back_populates="student"
    )
    teacher: Mapped[Optional["Teacher"]] = relationship(
        "Teacher", back_populates="student"
    )


class TeacherDialect(Base):
    __tablename__ = "teacher_dialects"

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "teacher.id", ondelete="CASCADE", name="teacher_dialects_teacher_id_fkey"
        ),
        primary_key=True,
    )

    dialect_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "dialects.id", ondelete="CASCADE", name="teacher_dialects_dialect_id_fkey"
        ),
        primary_key=True,
        index=True,
    )
