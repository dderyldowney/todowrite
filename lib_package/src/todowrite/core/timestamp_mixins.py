"""ToDoWrite Timestamp Utilities.

This module provides optimized timestamp handling for all ToDoWrite models.
It centralizes timestamp logic, improves performance, and ensures consistent
timezone-aware datetime handling across the monorepo.

Key Features:
- Optimized datetime factory functions for better performance
- Timezone-aware timestamps using UTC
- Reusable timestamp column mixins
- Consistent timestamp patterns across all models
- Performance optimizations for high-frequency operations

Example:
    >>> from todowrite.core.timestamp_mixins import TimestampMixin
    >>> from todowrite.core.timestamp_mixins import utc_now_factory

    # Use in model definitions
    class MyModel(Base, TimestampMixin):
        __tablename__ = "my_models"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String)

    # Use factory for optimized timestamps
    current_time = utc_now_factory()
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from collections.abc import Callable


# Optimized datetime factory for better performance
# This avoids repeated datetime.now() calls in column defaults
def utc_now_factory() -> Callable[[], datetime]:
    """Factory function that creates optimized UTC datetime callbacks.

    Returns a callable that can be used as a default value for SQLAlchemy
    DateTime columns. This is more performant than using datetime.utcnow
    directly as it avoids repeated function calls during column definition.

    Returns:
        Callable[[], datetime]: Function that returns current UTC datetime
    """

    def _utc_now() -> datetime:
        return datetime.now(UTC)

    return _utc_now


class TimestampMixin:
    """
    Mixin class providing standardized timestamp fields for SQLAlchemy models.

    This mixin adds created_at and updated_at columns to any model that
    inherits from it, ensuring consistent timestamp handling across all
    ToDoWrite models. The timestamps are automatically managed and
    timezone-aware using UTC.

    Usage:
        class MyModel(Base, TimestampMixin):
            __tablename__ = "my_models"
            id: Mapped[int] = mapped_column(primary_key=True)

    The resulting model will have:
        - created_at: Set automatically on record creation
        - updated_at: Set on creation and updated on record modification
    """

    # Use optimized factory for better performance
    # These columns are automatically managed by SQLAlchemy
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now_factory(),
        nullable=False,
        comment="Timestamp when record was created (UTC)",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now_factory(),
        onupdate=utc_now_factory(),
        nullable=False,
        comment="Timestamp when record was last updated (UTC)",
    )


class SoftDeleteMixin:
    """
    Mixin class providing soft delete functionality for SQLAlchemy models.

    This mixin adds deleted_at column to enable soft deletes while maintaining
    data integrity and audit trails. Records are not actually deleted from the
    database but marked with a deletion timestamp.

    Usage:
        class MyModel(Base, TimestampMixin, SoftDeleteMixin):
            __tablename__ = "my_models"
            id: Mapped[int] = mapped_column(primary_key=True)

    Query for active records:
        session.query(MyModel).filter(MyModel.deleted_at.is_(None))

    Query for deleted records:
        session.query(MyModel).filter(MyModel.deleted_at.is_not(None))
    """

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
        comment="Timestamp when record was soft deleted (UTC)",
    )


def create_timestamp_column(
    nullable: bool = False,
    default: bool = True,
    onupdate: bool = False,
    comment: str | None = None,
) -> Mapped[datetime]:
    """
    Factory function for creating timestamp columns with consistent configuration.

    This utility function provides a standardized way to create timestamp
    columns with common configurations, reducing code duplication and
    ensuring consistency across models.

    Args:
        nullable: Whether the column can be NULL (default: False)
        default: Whether to set default value to current timestamp (default: True)
        onupdate: Whether to update timestamp on record modification (default: False)
        comment: Optional comment for the column

    Returns:
        Mapped[datetime]: Configured timestamp column mapping

    Example:
        # Created timestamp (default on creation only)
        created_at = create_timestamp_column(
            default=True, onupdate=False,
            comment="Timestamp when record was created"
        )

        # Updated timestamp (default and onupdate)
        updated_at = create_timestamp_column(
            default=True, onupdate=True,
            comment="Timestamp when record was last updated"
        )

        # Optional timestamp
        archived_at = create_timestamp_column(
            nullable=True, default=False,
            comment="Timestamp when record was archived"
        )
    """
    column_kwargs: dict[str, str | int | bool] = {
        "nullable": nullable,
    }

    if default:
        column_kwargs["default"] = utc_now_factory()

    if onupdate:
        column_kwargs["onupdate"] = utc_now_factory()

    if comment:
        column_kwargs["comment"] = comment

    return mapped_column(DateTime, **column_kwargs)


class _TimestampCache:
    """
    Internal cache for optimizing high-frequency timestamp operations.

    This class provides a caching mechanism for timestamps to improve
    performance in scenarios where many records are created within
    the same second or operation batch.
    """

    def __init__(self, cache_duration_ms: int = 1000) -> None:
        """Initialize the timestamp cache.

        Args:
            cache_duration_ms: Duration to cache timestamps in milliseconds
        """
        self._cache_duration_ms = cache_duration_ms
        self._cached_timestamp: datetime | None = None
        self._cache_timestamp: datetime | None = None
        self._cache_hits = 0
        self._cache_misses = 0

    def now(self) -> datetime:
        """Get current timestamp with caching optimization.

        Returns cached timestamp if within cache duration, otherwise
        generates new timestamp and updates cache.

        Returns:
            datetime: Current UTC timestamp
        """
        current_time = datetime.now(UTC)

        if (
            self._cached_timestamp is None
            or self._cache_timestamp is None
            or (current_time - self._cache_timestamp).total_seconds() * 1000
            > self._cache_duration_ms
        ):
            self._cached_timestamp = current_time
            self._cache_timestamp = current_time
            self._cache_misses += 1
        else:
            self._cache_hits += 1

        return self._cached_timestamp

    @property
    def cache_stats(self) -> dict[str, int | str | float]:
        """Get cache performance statistics.

        Returns:
            dict containing cache hit/miss statistics and hit ratio
        """
        total_requests = self._cache_hits + self._cache_misses
        hit_ratio = (
            self._cache_hits / total_requests if total_requests > 0 else 0.0
        )

        return {
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "hit_ratio": hit_ratio,
            "total_requests": total_requests,
        }


# Global timestamp cache instance for use across the application
_timestamp_cache = _TimestampCache()


def get_optimized_timestamp() -> datetime:
    """
    Get optimized current timestamp using caching for high-frequency operations.

    This function provides a performance-optimized way to get current timestamps
    in scenarios where many records are created within short time periods.
    It uses a brief caching mechanism to reduce system calls.

    Returns:
        datetime: Current UTC timestamp (optimized)
    """
    return _timestamp_cache.now()


def validate_timezone_aware(dt: datetime) -> bool:
    """
    Validate that a datetime object is timezone-aware and in UTC.

    Args:
        dt: Datetime object to validate

    Returns:
        bool: True if datetime is timezone-aware and in UTC, False otherwise

    Example:
        >>> utc_dt = datetime.now(UTC)
        >>> validate_timezone_aware(utc_dt)
        True

        >>> naive_dt = datetime.now()
        >>> validate_timezone_aware(naive_dt)
        False
    """
    return dt.tzinfo is not None and dt.tzinfo == UTC


def convert_to_utc(dt: datetime) -> datetime:
    """
    Convert a datetime object to UTC timezone.

    Handles both naive and timezone-aware datetime objects,
    ensuring consistent UTC timezone handling.

    Args:
        dt: Datetime object to convert

    Returns:
        datetime: Datetime object in UTC timezone

    Raises:
        ValueError: If datetime object cannot be converted to UTC

    Example:
        >>> from datetime import timezone
        >>> local_dt = datetime.now(timezone.utc)
        >>> utc_dt = convert_to_utc(local_dt)
        >>> utc_dt.tzinfo == UTC
        True
    """
    if dt.tzinfo is None:
        # Assume naive datetime is in UTC
        return dt.replace(tzinfo=UTC)
    else:
        # Convert to UTC
        return dt.astimezone(UTC)


def format_timestamp_iso(dt: datetime) -> str:
    """
    Format datetime as ISO 8601 string in UTC.

    Args:
        dt: Datetime object to format

    Returns:
        str: ISO 8601 formatted timestamp string

    Example:
        >>> dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=UTC)
        >>> format_timestamp_iso(dt)
        '2023-01-01T12:00:00+00:00'
    """
    return dt.isoformat()


def parse_timestamp_iso(timestamp_str: str) -> datetime:
    """
    Parse ISO 8601 timestamp string to datetime object.

    Args:
        timestamp_str: ISO 8601 formatted timestamp string

    Returns:
        datetime: Parsed datetime object in UTC

    Raises:
        ValueError: If timestamp string cannot be parsed

    Example:
        >>> ts = '2023-01-01T12:00:00+00:00'
        >>> dt = parse_timestamp_iso(ts)
        >>> dt.tzinfo == UTC
        True
    """
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return convert_to_utc(dt)
    except ValueError as e:
        raise ValueError(f"Invalid ISO 8601 timestamp: {timestamp_str}") from e


# Export commonly used items for easier importing
__all__ = [
    "SoftDeleteMixin",
    "TimestampMixin",
    "convert_to_utc",
    "create_timestamp_column",
    "format_timestamp_iso",
    "get_optimized_timestamp",
    "parse_timestamp_iso",
    "utc_now_factory",
    "validate_timezone_aware",
]
