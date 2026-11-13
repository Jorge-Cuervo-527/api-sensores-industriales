"""Modelos Pydantic para validación y serialización de sensores industriales."""
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

# Rangos válidos de operación por tipo de sensor: (mínimo, máximo)
RANGOS: dict[str, tuple[float, float]] = {
    "temperatura": (-10.0, 100.0),
    "presion": (0.0, 500.0),
    "vibracion": (0.0, 5.0),
}

TipoSensor = Literal["temperatura", "presion", "vibracion"]


class SensorBase(BaseModel):
    """Modelo base con los atributos esenciales de un sensor industrial."""

    tipo: TipoSensor = Field(
        ...,
        description="Tipo de sensor ('temperatura', 'presion' o 'vibracion')",
        examples=["temperatura"],
    )
    valor: float = Field(
        ...,
        description="Lectura numérica obtenida por el sensor",
        examples=[25.5],
    )
    ubicacion: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Ubicación física del sensor dentro de la planta",
        examples=["Caldera Principal - Sector Norte"],
    )
    fecha: datetime = Field(
        ...,
        description="Fecha y hora de la medición en formato ISO 8601",
        examples=["2026-11-11T08:00:00"],
    )

    @field_validator("valor")
    @classmethod
    def validar_rango(cls, valor: float, info: ValidationInfo) -> float:
        """Verifica que el valor esté dentro del rango permitido según el tipo de sensor.

        Args:
            valor: Valor numérico a evaluar.
            info: Información contextual del proceso de validación.

        Returns:
            float: El valor validado si se encuentra en el rango admisible.

        Raises:
            ValueError: Si el valor se encuentra fuera del rango permitido.
        """
        tipo = info.data.get("tipo")
        if tipo and tipo in RANGOS:
            minimo, maximo = RANGOS[tipo]
            if not (minimo <= valor <= maximo):
                raise ValueError(
                    f"El valor para '{tipo}' debe estar entre {minimo} y {maximo}."
                )
        return valor


class SensorCreate(SensorBase):
    """Modelo para la creación de un nuevo sensor en la base de datos."""

    pass


class SensorUpdate(BaseModel):
    """Modelo para actualizar atributos de un sensor existente."""

    valor: Optional[float] = Field(
        default=None,
        description="Nuevo valor de lectura del sensor",
        examples=[32.4],
    )
    ubicacion: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Nueva ubicación física del sensor",
        examples=["Tanque 4 - Área Sur"],
    )
    fecha: Optional[datetime] = Field(
        default=None,
        description="Nueva fecha y hora de la lectura en formato ISO 8601",
        examples=["2026-11-11T08:30:00"],
    )

    def validar_contra_tipo(self, tipo: str) -> None:
        """Valida que el valor ingresado cumpla con el rango del tipo de sensor provisto.

        Args:
            tipo: Tipo de sensor para consultar los límites permitidos.

        Raises:
            ValueError: Si el valor numérico no se ajusta a los límites admisibles.
        """
        if self.valor is not None and tipo in RANGOS:
            minimo, maximo = RANGOS[tipo]
            if not (minimo <= self.valor <= maximo):
                raise ValueError(
                    f"El valor para '{tipo}' debe estar entre {minimo} y {maximo}."
                )


class SensorOut(SensorBase):
    """Modelo de salida que incluye el identificador único del documento."""

    id: str = Field(..., description="Identificador único del sensor (ObjectId de MongoDB)")

    model_config = ConfigDict(from_attributes=True)
