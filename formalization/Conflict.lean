import Std
namespace BinaryUnitConflict
variable {V : Type}
def Model (edge : V → V → Prop) (neg : V → V) (truth : V → Prop) :=
  (∀ v, truth (neg v) ↔ ¬truth v) ∧ (∀ u v, edge u v → truth u → truth v)

inductive Path (edge : V → V → Prop) : V → V → Prop
  | here (u) : Path edge u u
  | next {u v w} : Path edge u v → edge v w → Path edge u w

theorem follow {edge : V → V → Prop} {neg : V → V} {truth : V → Prop}
    (model : Model edge neg truth) {u v} (h : Path edge u v) : truth u → truth v := by
  induction h with
  | here => exact id
  | next h e ih => exact fun hu => model.2 _ _ e (ih hu)

/-- The witnesses can coincide, giving a single inconsistent unit. -/
theorem two_sources (edge : V → V → Prop) (neg : V → V) (unit : V → Prop)
    (inv : ∀ v, neg (neg v) = v)
    (contra : ∀ u v, edge u v → edge (neg v) (neg u))
    (sat : ∃ truth, Model edge neg truth)
    (bad : ¬ ∃ truth, Model edge neg truth ∧ ∀ v, unit v → truth v) :
    ∃ u v, unit u ∧ unit v ∧ ¬ ∃ truth, Model edge neg truth ∧ truth u ∧ truth v := by
  classical
  let R (v : V) := ∃ u, unit u ∧ Path edge u v
  have closed {u v} (hu : R u) (e : edge u v) : R v := by
    obtain ⟨a,ha,p⟩ := hu
    exact ⟨a,ha,.next p e⟩
  have clash : ∃ v, R v ∧ R (neg v) := by
    apply Classical.byContradiction
    intro h
    apply bad
    obtain ⟨t,hm⟩ := sat
    let t' (v : V) := R v ∨ (¬R (neg v) ∧ t v)
    refine ⟨t',⟨?_,?_⟩,?_⟩
    · intro v
      have hc : ¬(R v ∧ R (neg v)) := fun hh => h ⟨v,hh⟩
      have hn := hm.1 v
      simp only [t',inv]
      grind
    · intro u v he hu
      rcases hu with hr | ⟨hn,ht⟩
      · exact Or.inl (closed hr he)
      · exact Or.inr ⟨fun hnv => hn (closed hnv (contra u v he)), hm.2 u v he ht⟩
    · exact fun v hv => Or.inl ⟨v,hv,.here v⟩
  obtain ⟨x,⟨u,hu,pu⟩,⟨v,hv,pv⟩⟩ := clash
  refine ⟨u,v,hu,hv,?_⟩
  rintro ⟨t,hm,tu,tv⟩
  exact (hm.1 x).mp (follow hm pv tv) (follow hm pu tu)
end BinaryUnitConflict
#print axioms BinaryUnitConflict.two_sources
