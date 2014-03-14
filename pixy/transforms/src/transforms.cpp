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
 * \brief Transforms an image to greyscale.
 * \param self Unused.
 * \param args Arguments as a Python tuple. Expects two strings (input, output).
 * \return None or NULL on error.
 */
static PyObject * transforms_greyscale(PyObject *self, PyObject *args);

/**
 * \brief Transforms an image to sepia.
 * \param self Unused.
 * \param args Arguments as a Python tuple. Expects two strings (input, output).
 * \return None or NULL on error.
 */
static PyObject * transforms_sepia(PyObject *self, PyObject *args);

/**
 * \brief The methods of the Python Module.
 */
static PyMethodDef methods[] =
{
	{"blur", transforms_blur, METH_VARARGS, "Blur an image."},
	{"invert", transforms_invert, METH_VARARGS, "Invert an image."},
	{"greyscale", transforms_greyscale, METH_VARARGS, "Tranform an image to greyscale."},
	{"sepia", transforms_sepia, METH_VARARGS, "Transform an image to sepia."},
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
transforms_greyscale(PyObject *self, PyObject *args)
{
	const char *input, *output;

	if (!PyArg_ParseTuple(args, "ss", &input, &output))
		return NULL;
	try
	{
		Image image(input);
		greyscale(image);
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
transforms_sepia(PyObject *self, PyObject *args)
{
	const char *input, *output;

	if (!PyArg_ParseTuple(args, "ss", &input, &output))
		return NULL;
	try
	{
		Image image(input);
		sepia(image);
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

	if (PyModule_AddObject(m, "error", error) == -1)
		return NULL;

	Py_INCREF(error);

	return m;
}
