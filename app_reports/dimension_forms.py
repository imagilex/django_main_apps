"""
Formularios para modelo DimensionReporte

Formularios
-----------
frmDimensionReporte
    Formulario Completo
    - dimension
    - esfera
    - padre
"""
from django import forms

from .dimension_models import DimensionReporte
from .dimension_models import ValidationError
from .dimension_models import validate_cstr_esfera_padre

class frmDimensionReporte(forms.ModelForm):
    """
    Formulario principal del modelo DimensionReporte

    Campos
    ------
    - dimension
    - esfera
    - padre
    """

    class Meta:
        model = DimensionReporte
        fields = [
            'dimension',
            'esfera',
            'padre',
        ]

    def is_valid(self):
        """
        Agrega la validacion de cstr_esfera_padre

        Returns
        -------
        boolean
            True si es un formulario válido, Falso en otro caso
        """
        valido = False
        try:
            valido = super(frmDimensionReporte, self).is_valid()
            obj = DimensionReporte(
                dimension = self.cleaned_data['dimension'],
                esfera = self.cleaned_data['esfera'],
                padre = self.cleaned_data['padre']
            )
            validate_cstr_esfera_padre(obj)
        except ValidationError as e:
            self.add_error(None, e)
            valido = False
        finally:
            return valido
