import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { ChevronLeftIcon, EyeCloseIcon, EyeIcon } from "../../icons";
import Label from "../form/Label";
import Input from "../form/input/InputField";
import Checkbox from "../form/input/Checkbox";
import { authService } from "../../services/auth.service"; // ← Usar el authService

export default function SignUpForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [isChecked, setIsChecked] = useState(false);
  const [error, setError] = useState("");

  // Form fields
  const [formData, setFormData] = useState({
    fname: "",
    lname: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Submit handler
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!isChecked) {
      setError("Debes aceptar los términos y condiciones.");
      return;
    }

    // Validación básica de contraseña
    if (formData.password.length < 6) {
      setError("La contraseña debe tener al menos 6 caracteres.");
      return;
    }

    setLoading(true);

    try {
      // Payload según tu backend
      const payload = {
        name: `${formData.fname} ${formData.lname}`, // Combinar nombre completo
        email: formData.email,
        password: formData.password,
        role: "citizen", // Rol por defecto
      };

      // Usar el authService que ya guarda tokens automáticamente
      await authService.register(payload);

      // Redirigir al dashboard (ya está autenticado)
      navigate("/");
    } catch (error: any) {
      console.error("Registration error:", error);
      
      // Manejar errores específicos del backend
      let errorMessage = "Hubo un error al crear la cuenta.";
      
      if (error.response?.data?.email) {
        errorMessage = `Email: ${error.response.data.email[0]}`;
      } else if (error.response?.data?.password) {
        errorMessage = `Contraseña: ${error.response.data.password[0]}`;
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col flex-1 w-full overflow-y-auto lg:w-1/2 no-scrollbar">
      <div className="w-full max-w-md mx-auto mb-5 sm:pt-10">
        <Link
          to="/"
          className="inline-flex items-center text-sm text-gray-500 transition-colors hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
        >
          <ChevronLeftIcon className="size-5" />
          Back to dashboard
        </Link>
      </div>

      <div className="flex flex-col justify-center flex-1 w-full max-w-md mx-auto">
        <div>
          <div className="mb-5 sm:mb-8">
            <h1 className="mb-2 font-semibold text-gray-800 text-title-sm dark:text-white/90 sm:text-title-md">
              Registro VRISA
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Crea tu cuenta para acceder al sistema de monitoreo
            </p>
          </div>

          <div>
            {/* Error Alert */}
            {error && (
              <div className="mb-4 rounded-lg bg-red-50 p-4 text-sm text-red-800 dark:bg-red-900 dark:text-red-200">
                <svg
                  className="mr-2 inline h-5 w-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="space-y-5">

                {/* First + Last Name */}
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
                  <div>
                    <Label>
                      Nombre<span className="text-error-500">*</span>
                    </Label>
                    <Input
                      type="text"
                      id="fname"
                      name="fname"
                      value={formData.fname}
                      onChange={handleChange}
                      placeholder="Ingresa tu nombre"
                      required
                      disabled={loading}
                    />
                  </div>

                  <div>
                    <Label>
                      Apellido<span className="text-error-500">*</span>
                    </Label>
                    <Input
                      type="text"
                      id="lname"
                      name="lname"
                      value={formData.lname}
                      onChange={handleChange}
                      placeholder="Ingresa tu apellido"
                      required
                      disabled={loading}
                    />
                  </div>
                </div>

                {/* Email */}
                <div>
                  <Label>
                    Email<span className="text-error-500">*</span>
                  </Label>
                  <Input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="ejemplo@correo.com"
                    required
                    disabled={loading}
                  />
                </div>

                {/* Password */}
                <div>
                  <Label>
                    Contraseña<span className="text-error-500">*</span>
                  </Label>

                  <div className="relative">
                    <Input
                      placeholder="Mínimo 6 caracteres"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      type={showPassword ? "text" : "password"}
                      required
                      disabled={loading}
                    />
                    <span
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute z-30 -translate-y-1/2 cursor-pointer right-4 top-1/2"
                    >
                      {showPassword ? (
                        <EyeIcon className="fill-gray-500 dark:fill-gray-400 size-5" />
                      ) : (
                        <EyeCloseIcon className="fill-gray-500 dark:fill-gray-400 size-5" />
                      )}
                    </span>
                  </div>
                </div>

                {/* Checkbox */}
                <div className="flex items-center gap-3">
                  <Checkbox
                    className="w-5 h-5"
                    checked={isChecked}
                    onChange={setIsChecked}
                  />
                  <p className="inline-block text-sm font-normal text-gray-500 dark:text-gray-400">
                    Al crear una cuenta aceptas los{" "}
                    <span className="text-gray-800 dark:text-white/90">
                      Términos y Condiciones
                    </span>{" "}
                    y nuestra{" "}
                    <span className="text-gray-800 dark:text-white">
                      Política de Privacidad
                    </span>
                  </p>
                </div>

                {/* Submit */}
                <div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="flex items-center justify-center w-full px-4 py-3 text-sm font-medium text-white transition rounded-lg bg-brand-500 shadow-theme-xs hover:bg-brand-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? "Creando cuenta..." : "Crear Cuenta"}
                  </button>
                </div>
              </div>
            </form>

            <div className="mt-5">
              <p className="text-sm font-normal text-center text-gray-700 dark:text-gray-400 sm:text-start">
                ¿Ya tienes una cuenta?{" "}
                <Link
                  to="/signin"
                  className="text-brand-500 hover:text-brand-600 dark:text-brand-400"
                >
                  Inicia Sesión
                </Link>
              </p>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}