import numpy
import marshmallow


class SamplesValuesValidator(object):
    """Class implementing validator for the sample values"""

    @classmethod
    def validate(cls, values):
        """
        Validates the sample values.

        :param values: values to be validated
        :type values: Any
        :return: validated values
        :rtype: Any
        """

        # Validate the sample values
        if values is None:
            raise marshmallow.ValidationError(f"Missing data for required field.", "samples.values")
        if not isinstance(values, numpy.ndarray):
            raise marshmallow.ValidationError(f"Not a valid numpy.array.", "samples.values")
        if values.size == 0:
            raise marshmallow.ValidationError(f"Empty numpy.array.", "samples.values")

        # Ensure the subjects-dimension for a rank-one array
        values = numpy.atleast_2d(values)

        # Return the validated sample values
        return values


class SamplesLabelsValidator(object):
    """Class implementing validator for the sample labels"""

    @classmethod
    def validate(cls, labels, values):
        """
        Validates the sample labels.

        :param labels: labels to be validated
        :type labels: Any
        :param values: values to be referenced
        :type values: Any
        :return: validated values
        :rtype: Any
        """

        # Validate the sample labels
        if labels:
            if not isinstance(labels, (tuple, list)):
                raise marshmallow.ValidationError(f"Not a valid (tuple, list).", "samples.labels")
            if not (len(labels) == values.shape[-1]):
                raise marshmallow.ValidationError(
                    f"Not a valid shape (must match the values). The API expects the same number of labels "
                    f"as the shape of the last dimension of the samples (for more information, check the "
                    f"documentation or the docstring for the featurizer resource (resources.featurizer).",
                    "samples.labels")

        # Return the validated sample labels
        return labels
