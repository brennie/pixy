/**
 * \file C Python module for doing transforms.
 */

#include <Python.h>

#include <stdexcept>

#include "transforms.h"

static const char* doc = "C Python module for doing transforms. Use pixy.transforms instead of this module.";

static PyObject * error;

/**
 * \brief Blur a given image.
 * \param self Unused.
 * \param args Arguments as a Python tuple. Expects two strings (input, output)
 *             and an integer greater than 0.
 * \return None or NULL on error.
 */
static PyObject * transforms_blur(PyObject *self, PyObject *args);

/**
 * \brief Invert a given image.
 * \param self Unused.
 * \param args Arguments as a Python tuple. Expects two strings (input, output).
 * \return None or NULL on error.
 */
static PyObject * transforms_invert(PyObject *self, PyObject *args);

/**
 * \brief Flip a given image.
 * \param self Unused.
 * \param args Arguments as a Python tuple. Expects two strings (input, output)
 *             and an integer between 0 and 1 inclusive.
 * \return None or NULL on error.
 */
static PyObject * transforms_flip(PyObject *self, PyObject *args);

/**
 * \brief Rotate a given image.
 * \param self Unused.
 * \param args Arguments as a Python tuple. Expects two strings (input, output)
 *             and an integer between 0 and 2 inclusive.
 * \return None or NULL on error.
 */
static PyObject * transforms_rotate(PyObject *self, PyObject *args);

/**
 * \brief The methods of the Python Module.
 */
static PyMethodDef methods[] =
{
	{"blur", transforms_blur, METH_VARARGS, "Blur an image."},
	{"invert", transforms_invert, METH_VARARGS, "Invert an image."},
	{"flip", transforms_flip, METH_VARARGS, "Flip an image."},
	{"rotate", transforms_rotate, METH_VARARGS, "Rotate an image."},
	{NULL, NULL, 0, NULL}
};

/**
 * \brief The Python module.
 */
static struct PyModuleDef module =
{
	PyModuleDef_HEAD_INIT,
	"transforms",
	doc,
	-1,
	methods
};

static PyObject *
transforms_blur(PyObject *self, PyObject *args)
{
	const char *input, *output;
	int radius;

	if (!PyArg_ParseTuple(args, "ssi", &input, &output, &radius))
		return NULL;

	if (radius < 0)
	{
		PyErr_SetString(error, "radius must be > 0");
		return NULL;
	}

	try
	{
		Image image(input);
		blur(image, radius);
		image.save(output);
	}
	catch (const std::runtime_error &e)
	{
		PyErr_SetString(error, e.what());
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyObject *
transforms_invert(PyObject *self, PyObject *args)
{
	const char *input, *output;

	if (!PyArg_ParseTuple(args, "ss", &input, &output))
		return NULL;

	try
	{
		Image image(input);
		invert(image);
		image.save(output);
	}
	catch (const std::runtime_error &e)
	{
		PyErr_SetString(error, e.what());
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyObject *
transforms_flip(PyObject *self, PyObject *args)
{
	const char *input, *output;
	int theFlip;

	if (!PyArg_ParseTuple(args, "ssi", &input, &output, &theFlip))
		return NULL;

	if (theFlip < static_cast<int>(Flip::Horizontal) || theFlip > static_cast<int>(Flip::Vertical))
	{
		PyErr_SetString(error, "flip must be either FLIP_HORIZONTAL or FLIP_VERTICAL");
		return NULL;
	}

	try
	{
		Image image(input);
		flip(image, Flip(theFlip));
		image.save(output);
	}
	catch (const std::runtime_error &e)
	{
		PyErr_SetString(error, e.what());
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyObject *
transforms_rotate(PyObject *self, PyObject *args)
{
	const char *input, *output;
	int rotation;

	if (!PyArg_ParseTuple(args, "ssi", &input, &output, &rotation))
		return NULL;

	if (rotation < static_cast<int>(Rotation::Quarter) || rotation > static_cast<int>(Rotation::ThreeQuarter))
	{
		PyErr_SetString(error, "rotation must be ROTATION_QUARTER, ROTATION_HALF, or ROTATION_THREE_QUARTER");
		return NULL;
	}

	try
	{
		Image image(input);
		rotate(image, Rotation(rotation));
		image.save(output);
	}
	catch (const std::runtime_error &e)
	{
		PyErr_SetString(error, e.what());
		return NULL;
	}

	Py_RETURN_NONE;
}

/**
 * Initialize the Python Module
 * \return The created module or NULL.
 */
PyMODINIT_FUNC
PyInit_transforms()
{
	PyObject* m = PyModule_Create(&module);
	
	if (m == NULL)
		return m;

	error = PyErr_NewException("pixy.transforms.error", NULL, NULL);

	if (PyModule_AddObject(m, "error", error) == -1) return NULL;

	/* Flip constants. */
	if (PyModule_AddIntConstant(m, "FLIP_HORIZONTAL", static_cast<int>(Flip::Horizontal)) == -1)
		return NULL;
	if (PyModule_AddIntConstant(m, "FLIP_VERTICAL", static_cast<int>(Flip::Vertical)) == -1)
		return NULL;

	/* Rotation constants. */
	if (PyModule_AddIntConstant(m, "ROTATION_QUARTER", static_cast<int>(Rotation::Quarter)) == -1)
		return NULL;
	if (PyModule_AddIntConstant(m, "ROTATION_HALF", static_cast<int>(Rotation::Half)) == -1)
		return NULL;
	if (PyModule_AddIntConstant(m, "ROTATION_THREE_QUARTER", static_cast<int>(Rotation::ThreeQuarter)) == -1)
		return NULL;

	Py_INCREF(error);

	return m;
}
