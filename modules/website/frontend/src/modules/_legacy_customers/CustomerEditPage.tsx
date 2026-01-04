  const CustomerEditPage: React.FC = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState<CustomerEditFormState>(EMPTY_EDIT_FORM)
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

useEffect(() => {
  const load = async () => {
    if (!id) return

    setLoading(true)
    setError(null)

    try {
      const data = await apiFetch<CustomerDetail>(
        `/api/admin/customers/${id}`
      )

      setForm({
        email: data.email || '',
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        phone_number: data.phone_number || '',
        customer_type: data.customer_type,
        description: data.description || '',
        company_name: data.company_name || '',
        tax_id: data.tax_id || '',
        address_street: data.address_street || '',
        address_ext_number: data.address_ext_number || '',
        address_int_number: data.address_int_number || '',
        address_neighborhood: data.address_neighborhood || '',
        address_city: data.address_city || '',
        address_state: data.address_state || '',
        address_postal_code: data.address_postal_code || '',
        address_country: data.address_country || '',
      })
    } catch (err) {
      console.error(err)
      setError('Kon klantgegevens niet laden.')
    } finally {
      setLoading(false)
    }
  }

  load()
}, [id])

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const validate = (): string | null => {
    if (!form.first_name.trim()) return 'Voornaam is verplicht.'
    if (!form.last_name.trim()) return 'Achternaam is verplicht.'
    if (!form.email.trim()) return 'Email is verplicht.'
    if (!form.customer_type) return 'Klanttype is verplicht.'
    if (form.customer_type === 'bedrijf') {
      if (!form.company_name.trim() || !form.tax_id.trim()) {
        return 'Bedrijfsnaam en BTW/Tax ID zijn verplicht voor bedrijven.'
      }
    }
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setSuccess(null)

    const validationError = validate()
    if (validationError) {
      setError(validationError)
      return
    }

    setSaving(true)
    try {
      await apiFetch<void>(`/api/admin/customers/${id}`, {
        method: 'PUT',
        body: JSON.stringify(form),
      })

      setSuccess('Klantgegevens zijn opgeslagen.')
    } catch (err: any) {
      if (err.message === 'unauthorized') {
        setStoredToken(null)
        navigate('/login')
        return
      }
      console.error(err)
      setError('Kon klantgegevens niet opslaan.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return <p style={{ fontSize: '0.9rem' }}>Klantgegevens laden...</p>
  }

  return (
    <div>
      <button
        type="button"
        onClick={() => navigate('/customers')}
        style={{
          marginBottom: '0.75rem',
          padding: '0.35rem 0.7rem',
          borderRadius: 4,
          border: '1px solid #d1d5db',
          backgroundColor: '#f9fafb',
          fontSize: '0.85rem',
          cursor: 'pointer',
        }}
      >
        ← Terug naar klanten
      </button>

      <h1
        style={{
          fontSize: '1.1rem',
          fontWeight: 600,
          marginBottom: '0.5rem',
        }}
      >
        Klant bewerken
      </h1>

      {error && (
        <div
          style={{
            marginBottom: '0.75rem',
            padding: '0.5rem 0.75rem',
            borderRadius: 4,
            backgroundColor: '#fee2e2',
            color: '#991b1b',
            fontSize: '0.85rem',
          }}
        >
          {error}
        </div>
      )}

      {success && (
        <div
          style={{
            marginBottom: '0.75rem',
            padding: '0.5rem 0.75rem',
            borderRadius: 4,
            backgroundColor: '#dcfce7',
            color: '#166534',
            fontSize: '0.85rem',
          }}
        >
          {success}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        style={{
          backgroundColor: '#fff',
          padding: '0.75rem 0.9rem',
          borderRadius: 6,
          boxShadow: '0 1px 2px rgba(15,23,42,0.05)',
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '0.75rem',
          }}
        >
          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Voornaam
            </label>
            <input
              type="text"
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Achternaam
            </label>
            <input
              type="text"
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Email
            </label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Telefoon
            </label>
            <input
              type="text"
              name="phone_number"
              value={form.phone_number}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Klanttype
            </label>
            <select
              name="customer_type"
              value={form.customer_type}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            >
              <option value="particulier">Particulier</option>
              <option value="bedrijf">Bedrijf</option>
            </select>
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Bedrijfsnaam
            </label>
            <input
              type="text"
              name="company_name"
              value={form.company_name}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              BTW / Tax ID
            </label>
            <input
              type="text"
              name="tax_id"
              value={form.tax_id}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div style={{ gridColumn: '1 / -1' }}>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Omschrijving
            </label>
            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              rows={3}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
                resize: 'vertical',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Straat
            </label>
            <input
              type="text"
              name="address_street"
              value={form.address_street}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Huisnummer
            </label>
            <input
              type="text"
              name="address_ext_number"
              value={form.address_ext_number}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              App./Int. nummer
            </label>
            <input
              type="text"
              name="address_int_number"
              value={form.address_int_number}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Wijk / Colonia
            </label>
            <input
              type="text"
              name="address_neighborhood"
              value={form.address_neighborhood}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Stad
            </label>
            <input
              type="text"
              name="address_city"
              value={form.address_city}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Staat
            </label>
            <input
              type="text"
              name="address_state"
              value={form.address_state}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Postcode
            </label>
            <input
              type="text"
              name="address_postal_code"
              value={form.address_postal_code}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.85rem',
                marginBottom: '0.25rem',
              }}
            >
              Land
            </label>
            <input
              type="text"
              name="address_country"
              value={form.address_country}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.4rem 0.5rem',
                borderRadius: 4,
                border: '1px solid #d1d5db',
                fontSize: '0.9rem',
              }}
            />
          </div>
        </div>

        <div
          style={{
            marginTop: '0.75rem',
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '0.5rem',
          }}
        >
          <button
            type="button"
            onClick={() => navigate(`/customers/${id}`)}
            style={{
              padding: '0.4rem 0.75rem',
              borderRadius: 4,
              border: '1px solid #d1d5db',
              backgroundColor: '#f9fafb',
              fontSize: '0.9rem',
              cursor: 'pointer',
            }}
          >
            Annuleren
          </button>
          <button
            type="submit"
            disabled={saving}
            style={{
              padding: '0.4rem 0.75rem',
              borderRadius: 4,
              border: 'none',
              backgroundColor: '#2563eb',
              color: '#fff',
              fontSize: '0.9rem',
              fontWeight: 500,
              cursor: saving ? 'default' : 'pointer',
              opacity: saving ? 0.7 : 1,
            }}
          >
            {saving ? 'Bezig met opslaan...' : 'Opslaan'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default CustomerEditPage
