%------------------------------------------------------------------------------
% File     : ARI745_1 : TPTP v9.3.1. Released v7.0.0.
% Domain   : Software Verification
% Problem  : Aviation C program verification problem
% Version  : Especial.
% English  :

% Refs     :
% Source   : [SMTL]
% Names    : aviation/array_double_why.p [SMTL]

% Status   : Unsatisfiable
% Rating   : 0.00 v9.3.0, 0.50 v9.1.0, 0.40 v8.2.0, 0.50 v8.1.0, 0.67 v7.3.0, 0.75 v7.1.0, 0.67 v7.0.0
% Syntax   : Number of formulae    :  356 (  23 unt; 162 typ;   0 def)
%            Number of atoms       :  779 ( 529 equ)
%            Maximal formula atoms :   14 (   4 avg)
%            Number of connectives :  606 (  21   ~;   8   |; 440   &)
%                                         (  73 <=>;  64  =>;   0  <=;   0 <~>)
%            Maximal formula depth :   32 (   9 avg)
%            Maximal term depth    :    9 (   1 avg)
%            Number arithmetic     :  430 ( 107 atm;  35 fun;  68 num; 220 var)
%            Number of types       :    8 (   5 usr;   2 ari;   0 dat;   0 cdt)
%            Number of type conns  :  323 ( 137   >; 186   *;   0   +;   0  <<)
%            Number of predicates  :   52 (  47 usr;   0 prp; 1-8 aty)
%            Number of functors    :  121 ( 110 usr;  27 con; 0-5 aty)
%            Number of variables   :  973 ( 603   !; 370   ?; 973   :)
% SPC      : TF0_UNS_EQU_ARI_NDT

% Comments : This is an SMT-LIB AUFNIRA problem. 
%          : This problem comes from the verification of C programs using Why 
%            from the aviation industry.
%          : Translated to TFF using Peter Baumgartner's SMTtoTPTP program.
%------------------------------------------------------------------------------
tff(c_sorted,type,
    c_sorted: $tType ).

tff('Unit',type,
    'Unit': $tType ).

tff(c_unsorted,type,
    c_unsorted: $tType ).

tff(c_Boolean,type,
    c_Boolean: $tType ).

tff(c_type,type,
    c_type: $tType ).

tff(lsl,type,
    lsl: ( $int * $int ) > $int ).

tff(char_P_tag,type,
    char_P_tag: c_unsorted ).

tff(pset_union,type,
    pset_union: ( c_sorted * c_sorted ) > c_unsorted ).

tff(left_valid_struct_void_P,type,
    left_valid_struct_void_P: ( c_sorted * $int * c_sorted ) > $o ).

tff(int_of_tag,type,
    int_of_tag: c_sorted > $int ).

tff(bool_not,type,
    bool_not: c_Boolean > c_Boolean ).

tff(int_min,type,
    int_min: ( $int * $int ) > $int ).

tff(c_Boolean_true,type,
    c_Boolean_true: c_Boolean ).

tff(bitvector_of_char_P,type,
    bitvector_of_char_P: c_sorted > c_unsorted ).

tff(base_block,type,
    base_block: c_sorted > c_unsorted ).

tff(strict_valid_root_void_P,type,
    strict_valid_root_void_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(smtlib____anonstruct_T_CompositionPage_1_of_pointer_address,type,
    smtlib____anonstruct_T_CompositionPage_1_of_pointer_address: c_sorted > c_unsorted ).

tff(downcast,type,
    downcast: ( c_sorted * c_sorted * c_sorted ) > c_unsorted ).

tff(pset_empty,type,
    pset_empty: c_unsorted ).

tff(root_tag,type,
    root_tag: c_sorted > $o ).

tff(char__x__1__P,type,
    char__x__1__P: c_type ).

tff(pset_range,type,
    pset_range: ( c_sorted * $int * $int ) > c_unsorted ).

tff(strict_valid_struct_char__x__1__P,type,
    strict_valid_struct_char__x__1__P: ( c_sorted * $int * $int * c_sorted * c_sorted * c_sorted ) > $o ).

tff(right_valid_struct_char__x__1__P,type,
    right_valid_struct_char__x__1__P: ( c_sorted * $int * c_sorted * c_sorted * c_sorted ) > $o ).

tff(tag_table,type,
    tag_table: c_type > c_type ).

tff(alloc_extends,type,
    alloc_extends: ( c_sorted * c_sorted ) > $o ).

tff(int_max,type,
    int_max: ( $int * $int ) > $int ).

tff(c_unit,type,
    c_unit: c_type ).

tff(valid_root_void_P,type,
    valid_root_void_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(valid_struct_char_P,type,
    valid_struct_char_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(pset_deref,type,
    pset_deref: ( c_sorted * c_sorted ) > c_unsorted ).

tff(tag_id,type,
    tag_id: c_type > c_type ).

tff(offset_max_bytes,type,
    offset_max_bytes: ( c_sorted * c_sorted * $int ) > $int ).

tff(neq_int_bool,type,
    neq_int_bool: ( $int * $int ) > c_Boolean ).

tff(store_bytes,type,
    store_bytes: ( c_sorted * c_sorted * $int * $int * c_sorted ) > c_unsorted ).

tff(s2bool,type,
    s2bool: c_sorted > c_Boolean ).

tff(subtag_bool,type,
    subtag_bool: ( c_sorted * c_sorted ) > c_Boolean ).

tff(abs_real,type,
    abs_real: $real > $real ).

tff(replace_bytes,type,
    replace_bytes: ( c_sorted * $int * $int * c_sorted ) > c_unsorted ).

tff(neq_real_bool,type,
    neq_real_bool: ( $real * $real ) > c_Boolean ).

tff(char__x__1__P_tag,type,
    char__x__1__P_tag: c_unsorted ).

tff(abs_int,type,
    abs_int: $int > $int ).

tff(eq_int8,type,
    eq_int8: ( c_sorted * c_sorted ) > $o ).

tff(valid_struct_char__x__1__P,type,
    valid_struct_char__x__1__P: ( c_sorted * $int * $int * c_sorted * c_sorted * c_sorted ) > $o ).

tff(c_Boolean_false,type,
    c_Boolean_false: c_Boolean ).

tff(bool_or,type,
    bool_or: ( c_Boolean * c_Boolean ) > c_Boolean ).

tff(eq_real_bool,type,
    eq_real_bool: ( $real * $real ) > c_Boolean ).

tff(lt_real_bool,type,
    lt_real_bool: ( $real * $real ) > c_Boolean ).

tff(block,type,
    block: c_type > c_type ).

tff(left_valid_struct_char__x__1__P,type,
    left_valid_struct_char__x__1__P: ( c_sorted * $int * c_sorted * c_sorted * c_sorted ) > $o ).

tff(same_block,type,
    same_block: ( c_sorted * c_sorted ) > $o ).

tff(log,type,
    log: $real > $real ).

tff(pset_included,type,
    pset_included: ( c_sorted * c_sorted ) > $o ).

tff(pset,type,
    pset: c_type > c_type ).

tff(address,type,
    address: c_sorted > $int ).

tff(strict_valid_root_char_P,type,
    strict_valid_root_char_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(shift,type,
    shift: ( c_sorted * $int ) > c_unsorted ).

tff(in_pset,type,
    in_pset: ( c_sorted * c_sorted ) > $o ).

tff(exp,type,
    exp: $real > $real ).

tff(gt_int_bool,type,
    gt_int_bool: ( $int * $int ) > c_Boolean ).

tff(offset_min_bytes,type,
    offset_min_bytes: ( c_sorted * c_sorted * $int ) > $int ).

tff(instanceof,type,
    instanceof: ( c_sorted * c_sorted * c_sorted ) > $o ).

tff(null,type,
    null: c_unsorted ).

tff(alloc_extends_except,type,
    alloc_extends_except: ( c_sorted * c_sorted * c_sorted ) > $o ).

tff(valid_bitvector_struct_char__x__1__P,type,
    valid_bitvector_struct_char__x__1__P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(valid_struct___anonstruct_T_CompositionPage_1,type,
    valid_struct___anonstruct_T_CompositionPage_1: ( c_sorted * $int * $int * c_sorted * c_sorted * c_sorted * c_sorted * c_sorted ) > $o ).

tff(bitvector_of_char__x__1__P,type,
    bitvector_of_char__x__1__P: c_sorted > c_unsorted ).

tff(eq_pointer_bool,type,
    eq_pointer_bool: ( c_sorted * c_sorted ) > c_Boolean ).

tff(valid_bitvector_struct___anonstruct_T_CompositionPage_1,type,
    valid_bitvector_struct___anonstruct_T_CompositionPage_1: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(unit2u,type,
    unit2u: 'Unit' > c_unsorted ).

tff(pset_range_left,type,
    pset_range_left: ( c_sorted * $int ) > c_unsorted ).

tff(le_real_bool,type,
    le_real_bool: ( $real * $real ) > c_Boolean ).

tff(void_P_of_bitvector,type,
    void_P_of_bitvector: c_sorted > c_unsorted ).

tff(s2real,type,
    s2real: c_sorted > $real ).

tff(concat_bitvector,type,
    concat_bitvector: ( c_sorted * c_sorted ) > c_unsorted ).

tff(pset_range_right,type,
    pset_range_right: ( c_sorted * $int ) > c_unsorted ).

tff(int2u,type,
    int2u: $int > c_unsorted ).

tff(not_assigns,type,
    not_assigns: ( c_sorted * c_sorted * c_sorted * c_sorted ) > $o ).

tff(valid_bitvector_struct_char_P,type,
    valid_bitvector_struct_char_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(int8_of_integer,type,
    int8_of_integer: $int > c_unsorted ).

tff(s2unit,type,
    s2unit: c_sorted > 'Unit' ).

tff(s2int,type,
    s2int: c_sorted > $int ).

tff(void_P_of_pointer_address,type,
    void_P_of_pointer_address: c_sorted > c_unsorted ).

tff(c_real,type,
    c_real: c_type ).

tff(real_max,type,
    real_max: ( $real * $real ) > $real ).

tff(lt_int_bool,type,
    lt_int_bool: ( $int * $int ) > c_Boolean ).

tff(offset_max,type,
    offset_max: ( c_sorted * c_sorted ) > $int ).

tff(parenttag,type,
    parenttag: ( c_sorted * c_sorted ) > $o ).

tff(valid_pset,type,
    valid_pset: ( c_sorted * c_sorted ) > $o ).

tff(right_valid_struct_char_P,type,
    right_valid_struct_char_P: ( c_sorted * $int * c_sorted ) > $o ).

tff(smtlib__select,type,
    smtlib__select: ( c_sorted * c_sorted ) > c_unsorted ).

tff(smtlib____anonstruct_T_CompositionPage_1_of_bitvector,type,
    smtlib____anonstruct_T_CompositionPage_1_of_bitvector: c_sorted > c_unsorted ).

tff(strict_valid_struct___anonstruct_T_CompositionPage_1,type,
    strict_valid_struct___anonstruct_T_CompositionPage_1: ( c_sorted * $int * $int * c_sorted * c_sorted * c_sorted * c_sorted * c_sorted ) > $o ).

tff(eq_message,type,
    eq_message: ( c_sorted * $int ) > $o ).

tff(strict_valid_struct_char_P,type,
    strict_valid_struct_char_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(memory,type,
    memory: ( c_type * c_type ) > c_type ).

tff(real2u,type,
    real2u: $real > c_unsorted ).

tff(valid_bitvector_struct_void_P,type,
    valid_bitvector_struct_void_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(int8,type,
    int8: c_type ).

tff(right_valid_struct_void_P,type,
    right_valid_struct_void_P: ( c_sorted * $int * c_sorted ) > $o ).

tff(bw_and,type,
    bw_and: ( $int * $int ) > $int ).

tff(gt_real_bool,type,
    gt_real_bool: ( $real * $real ) > c_Boolean ).

tff(valid_root_char__x__1__P,type,
    valid_root_char__x__1__P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(c_sort,type,
    c_sort: ( c_type * c_unsorted ) > c_sorted ).

tff(offset_min,type,
    offset_min: ( c_sorted * c_sorted ) > $int ).

tff(typeof,type,
    typeof: ( c_sorted * c_sorted ) > c_unsorted ).

tff(bitvector_of_int8,type,
    bitvector_of_int8: c_sorted > c_unsorted ).

tff(void_P_tag,type,
    void_P_tag: c_unsorted ).

tff(char_P_of_pointer_address,type,
    char_P_of_pointer_address: c_sorted > c_unsorted ).

tff(le_int_bool,type,
    le_int_bool: ( $int * $int ) > c_Boolean ).

tff(valid,type,
    valid: ( c_sorted * c_sorted ) > $o ).

tff(bottom_tag,type,
    bottom_tag: c_unsorted ).

tff(smtlib____anonstruct_T_CompositionPage_1_tag,type,
    smtlib____anonstruct_T_CompositionPage_1_tag: c_unsorted ).

tff(bitvector,type,
    bitvector: c_type ).

tff(right_valid_struct___anonstruct_T_CompositionPage_1,type,
    right_valid_struct___anonstruct_T_CompositionPage_1: ( c_sorted * $int * c_sorted * c_sorted * c_sorted * c_sorted * c_sorted ) > $o ).

tff(full_separated,type,
    full_separated: ( c_sorted * c_sorted ) > $o ).

tff(valid_Page,type,
    valid_Page: c_sorted > $o ).

tff(integer_of_int8,type,
    integer_of_int8: c_sorted > $int ).

tff(lsr,type,
    lsr: ( $int * $int ) > $int ).

tff(pset_all,type,
    pset_all: c_sorted > c_unsorted ).

tff(pointer_address,type,
    pointer_address: c_sorted > c_unsorted ).

tff(extract_bytes,type,
    extract_bytes: ( c_sorted * $int * $int ) > c_unsorted ).

tff(bool_and,type,
    bool_and: ( c_Boolean * c_Boolean ) > c_Boolean ).

tff(strict_valid_struct_void_P,type,
    strict_valid_struct_void_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(smtlib__ite,type,
    smtlib__ite: ( c_Boolean * c_sorted * c_sorted ) > c_unsorted ).

tff(valid_root_char_P,type,
    valid_root_char_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(fully_packed,type,
    fully_packed: ( c_sorted * c_sorted * c_sorted ) > $o ).

tff(bool_xor,type,
    bool_xor: ( c_Boolean * c_Boolean ) > c_Boolean ).

tff(alloc_fresh,type,
    alloc_fresh: ( c_sorted * c_sorted * $int ) > $o ).

tff(bitvector_of___anonstruct_T_CompositionPage_1,type,
    bitvector_of___anonstruct_T_CompositionPage_1: c_sorted > c_unsorted ).

tff(char__x__1__P_of_bitvector,type,
    char__x__1__P_of_bitvector: c_sorted > c_unsorted ).

tff(ge_real_bool,type,
    ge_real_bool: ( $real * $real ) > c_Boolean ).

tff(left_valid_struct___anonstruct_T_CompositionPage_1,type,
    left_valid_struct___anonstruct_T_CompositionPage_1: ( c_sorted * $int * c_sorted * c_sorted * c_sorted * c_sorted * c_sorted ) > $o ).

tff(eq_int_bool,type,
    eq_int_bool: ( $int * $int ) > c_Boolean ).

tff(char__x__1__P_of_pointer_address,type,
    char__x__1__P_of_pointer_address: c_sorted > c_unsorted ).

tff(strict_valid_root_char__x__1__P,type,
    strict_valid_root_char__x__1__P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(c_bool,type,
    c_bool: c_type ).

tff(subtag,type,
    subtag: ( c_sorted * c_sorted ) > $o ).

tff(pset_singleton,type,
    pset_singleton: c_sorted > c_unsorted ).

tff(bitvector_of_void_P,type,
    bitvector_of_void_P: c_sorted > c_unsorted ).

tff(pointer,type,
    pointer: c_type > c_type ).

tff(valid_struct_void_P,type,
    valid_struct_void_P: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(valid_root___anonstruct_T_CompositionPage_1,type,
    valid_root___anonstruct_T_CompositionPage_1: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(smtlib____anonstruct_T_CompositionPage_1,type,
    smtlib____anonstruct_T_CompositionPage_1: c_type ).

tff(select_bytes,type,
    select_bytes: ( c_sorted * c_sorted * $int * $int ) > c_unsorted ).

tff(bool2u,type,
    bool2u: c_Boolean > c_unsorted ).

tff(void_P,type,
    void_P: c_type ).

tff(char_P_of_bitvector,type,
    char_P_of_bitvector: c_sorted > c_unsorted ).

tff(asr,type,
    asr: ( $int * $int ) > $int ).

tff(c_int,type,
    c_int: c_type ).

tff('Page',type,
    'Page': c_unsorted ).

tff(neq_pointer_bool,type,
    neq_pointer_bool: ( c_sorted * c_sorted ) > c_Boolean ).

tff(pset_disjoint,type,
    pset_disjoint: ( c_sorted * c_sorted ) > $o ).

tff(int8_of_bitvector,type,
    int8_of_bitvector: c_sorted > c_unsorted ).

tff(alloc_table,type,
    alloc_table: c_type > c_type ).

tff(sub_pointer,type,
    sub_pointer: ( c_sorted * c_sorted ) > $int ).

tff(strict_valid_root___anonstruct_T_CompositionPage_1,type,
    strict_valid_root___anonstruct_T_CompositionPage_1: ( c_sorted * $int * $int * c_sorted ) > $o ).

tff(char_P,type,
    char_P: c_type ).

tff(real_min,type,
    real_min: ( $real * $real ) > $real ).

tff(ge_int_bool,type,
    ge_int_bool: ( $int * $int ) > c_Boolean ).

tff(left_valid_struct_char_P,type,
    left_valid_struct_char_P: ( c_sorted * $int * c_sorted ) > $o ).

tff(smtlib__store,type,
    smtlib__store: ( c_sorted * c_sorted * c_sorted ) > c_unsorted ).

tff(formula_1,axiom,
    ! [A__questionmark_bcd: c_Boolean] :
      ( ( A__questionmark_bcd = c_Boolean_true )
      | ( A__questionmark_bcd = c_Boolean_false ) ) ).

tff(formula_2,axiom,
    c_Boolean_true != c_Boolean_false ).

tff(formula_3,axiom,
    ! [A__questionmark_xu0_1: $int] : ( s2int(c_sort(c_int,int2u(A__questionmark_xu0_1))) = A__questionmark_xu0_1 ) ).

tff(formula_4,axiom,
    ! [A__questionmark_xu0_2: c_Boolean] : ( s2bool(c_sort(c_bool,bool2u(A__questionmark_xu0_2))) = A__questionmark_xu0_2 ) ).

tff(formula_5,axiom,
    ! [A__questionmark_xu0_3: $real] : ( s2real(c_sort(c_real,real2u(A__questionmark_xu0_3))) = A__questionmark_xu0_3 ) ).

tff(formula_6,axiom,
    ! [A__questionmark_xu0_4: 'Unit'] : ( s2unit(c_sort(c_unit,unit2u(A__questionmark_xu0_4))) = A__questionmark_xu0_4 ) ).

tff(formula_7,axiom,
    ! [A__questionmark_xu0_5: c_unsorted] : ( int2u(s2int(c_sort(c_int,A__questionmark_xu0_5))) = A__questionmark_xu0_5 ) ).

tff(formula_8,axiom,
    ! [A__questionmark_xu0_6: c_unsorted] : ( bool2u(s2bool(c_sort(c_bool,A__questionmark_xu0_6))) = A__questionmark_xu0_6 ) ).

tff(formula_9,axiom,
    ! [A__questionmark_xu0_7: c_unsorted] : ( real2u(s2real(c_sort(c_real,A__questionmark_xu0_7))) = A__questionmark_xu0_7 ) ).

tff(formula_10,axiom,
    ! [A__questionmark_xu0_8: c_unsorted] : ( unit2u(s2unit(c_sort(c_unit,A__questionmark_xu0_8))) = A__questionmark_xu0_8 ) ).

tff(formula_11,axiom,
    ! [A__questionmark_au0_9: $int,A__questionmark_bu0_10: $int] :
      ( ( $lesseq(0,A__questionmark_bu0_10)
        & $less(A__questionmark_au0_9,A__questionmark_bu0_10) )
    <=> ( $lesseq(0,A__questionmark_bu0_10)
        & $less(A__questionmark_au0_9,A__questionmark_bu0_10) ) ) ).

tff(formula_12,axiom,
    ! [A__questionmark_au33_11: c_Boolean,A__questionmark_bu32_12: c_Boolean] :
      ( ( bool_and(A__questionmark_au33_11,A__questionmark_bu32_12) = c_Boolean_true )
    <=> ( ( A__questionmark_au33_11 = c_Boolean_true )
        & ( A__questionmark_bu32_12 = c_Boolean_true ) ) ) ).

tff(formula_13,axiom,
    ! [A__questionmark_au35_13: c_Boolean,A__questionmark_bu34_14: c_Boolean] :
      ( ( bool_or(A__questionmark_au35_13,A__questionmark_bu34_14) = c_Boolean_true )
    <=> ( ( A__questionmark_au35_13 = c_Boolean_true )
        | ( A__questionmark_bu34_14 = c_Boolean_true ) ) ) ).

tff(formula_14,axiom,
    ! [A__questionmark_au37_15: c_Boolean,A__questionmark_bu36_16: c_Boolean] :
      ( ( bool_xor(A__questionmark_au37_15,A__questionmark_bu36_16) = c_Boolean_true )
    <=> ( A__questionmark_au37_15 != A__questionmark_bu36_16 ) ) ).

tff(formula_15,axiom,
    ! [A__questionmark_au38_17: c_Boolean] :
      ( ( bool_not(A__questionmark_au38_17) = c_Boolean_true )
    <=> ( A__questionmark_au38_17 = c_Boolean_false ) ) ).

tff(formula_16,axiom,
    ! [A__questionmark_t1u0_18: c_type,A__questionmark_xu40_19: c_unsorted,A__questionmark_yu39_20: c_unsorted] :
    ? [A__questionmark_v_0_2: c_sorted] :
      ( ( A__questionmark_v_0_2 = c_sort(A__questionmark_t1u0_18,A__questionmark_xu40_19) )
      & ( c_sort(A__questionmark_t1u0_18,smtlib__ite(c_Boolean_true,A__questionmark_v_0_2,c_sort(A__questionmark_t1u0_18,A__questionmark_yu39_20))) = A__questionmark_v_0_2 ) ) ).

tff(formula_17,axiom,
    ! [A__questionmark_t1u0_21: c_type,A__questionmark_xu42_22: c_unsorted,A__questionmark_yu41_23: c_unsorted] :
    ? [A__questionmark_v_0_3: c_sorted] :
      ( ( A__questionmark_v_0_3 = c_sort(A__questionmark_t1u0_21,A__questionmark_yu41_23) )
      & ( c_sort(A__questionmark_t1u0_21,smtlib__ite(c_Boolean_false,c_sort(A__questionmark_t1u0_21,A__questionmark_xu42_22),A__questionmark_v_0_3)) = A__questionmark_v_0_3 ) ) ).

tff(formula_18,axiom,
    ! [A__questionmark_xu45_24: $int,A__questionmark_yu44_25: $int] :
      ( ( lt_int_bool(A__questionmark_xu45_24,A__questionmark_yu44_25) = c_Boolean_true )
    <=> $less(A__questionmark_xu45_24,A__questionmark_yu44_25) ) ).

tff(formula_19,axiom,
    ! [A__questionmark_xu47_26: $int,A__questionmark_yu46_27: $int] :
      ( ( le_int_bool(A__questionmark_xu47_26,A__questionmark_yu46_27) = c_Boolean_true )
    <=> $lesseq(A__questionmark_xu47_26,A__questionmark_yu46_27) ) ).

tff(formula_20,axiom,
    ! [A__questionmark_xu49_28: $int,A__questionmark_yu48_29: $int] :
      ( ( gt_int_bool(A__questionmark_xu49_28,A__questionmark_yu48_29) = c_Boolean_true )
    <=> $greater(A__questionmark_xu49_28,A__questionmark_yu48_29) ) ).

tff(formula_21,axiom,
    ! [A__questionmark_xu51_30: $int,A__questionmark_yu50_31: $int] :
      ( ( ge_int_bool(A__questionmark_xu51_30,A__questionmark_yu50_31) = c_Boolean_true )
    <=> $greatereq(A__questionmark_xu51_30,A__questionmark_yu50_31) ) ).

tff(formula_22,axiom,
    ! [A__questionmark_xu53_32: $int,A__questionmark_yu52_33: $int] :
      ( ( eq_int_bool(A__questionmark_xu53_32,A__questionmark_yu52_33) = c_Boolean_true )
    <=> ( A__questionmark_xu53_32 = A__questionmark_yu52_33 ) ) ).

tff(formula_23,axiom,
    ! [A__questionmark_xu55_34: $int,A__questionmark_yu54_35: $int] :
      ( ( neq_int_bool(A__questionmark_xu55_34,A__questionmark_yu54_35) = c_Boolean_true )
    <=> ( A__questionmark_xu55_34 != A__questionmark_yu54_35 ) ) ).

tff(formula_24,axiom,
    ! [A__questionmark_xu56_36: $int] :
      ( $greatereq(A__questionmark_xu56_36,0)
     => ( abs_int(A__questionmark_xu56_36) = A__questionmark_xu56_36 ) ) ).

tff(formula_25,axiom,
    ! [A__questionmark_xu57_37: $int] :
      ( $lesseq(A__questionmark_xu57_37,0)
     => ( abs_int(A__questionmark_xu57_37) = $uminus(A__questionmark_xu57_37) ) ) ).

tff(formula_26,axiom,
    ! [A__questionmark_xu59_38: $int,A__questionmark_yu58_39: $int] :
    ? [A__questionmark_v_0_4: $int] :
      ( ( A__questionmark_v_0_4 = int_max(A__questionmark_xu59_38,A__questionmark_yu58_39) )
      & $greatereq(A__questionmark_v_0_4,A__questionmark_xu59_38)
      & $greatereq(A__questionmark_v_0_4,A__questionmark_yu58_39) ) ).

tff(formula_27,axiom,
    ! [A__questionmark_xu61_40: $int,A__questionmark_yu60_41: $int] :
    ? [A__questionmark_v_0_5: $int] :
      ( ( A__questionmark_v_0_5 = int_max(A__questionmark_xu61_40,A__questionmark_yu60_41) )
      & ( ( A__questionmark_v_0_5 = A__questionmark_xu61_40 )
        | ( A__questionmark_v_0_5 = A__questionmark_yu60_41 ) ) ) ).

tff(formula_28,axiom,
    ! [A__questionmark_xu63_42: $int,A__questionmark_yu62_43: $int] :
    ? [A__questionmark_v_0_6: $int] :
      ( ( A__questionmark_v_0_6 = int_min(A__questionmark_xu63_42,A__questionmark_yu62_43) )
      & $lesseq(A__questionmark_v_0_6,A__questionmark_xu63_42)
      & $lesseq(A__questionmark_v_0_6,A__questionmark_yu62_43) ) ).

tff(formula_29,axiom,
    ! [A__questionmark_xu65_44: $int,A__questionmark_yu64_45: $int] :
    ? [A__questionmark_v_0_7: $int] :
      ( ( A__questionmark_v_0_7 = int_min(A__questionmark_xu65_44,A__questionmark_yu64_45) )
      & ( ( A__questionmark_v_0_7 = A__questionmark_xu65_44 )
        | ( A__questionmark_v_0_7 = A__questionmark_yu64_45 ) ) ) ).

tff(formula_30,axiom,
    ! [A__questionmark_xu82_46: $real,A__questionmark_yu81_47: $real] :
      ( ( lt_real_bool(A__questionmark_xu82_46,A__questionmark_yu81_47) = c_Boolean_true )
    <=> $less(A__questionmark_xu82_46,A__questionmark_yu81_47) ) ).

tff(formula_31,axiom,
    ! [A__questionmark_xu84_48: $real,A__questionmark_yu83_49: $real] :
      ( ( le_real_bool(A__questionmark_xu84_48,A__questionmark_yu83_49) = c_Boolean_true )
    <=> $lesseq(A__questionmark_xu84_48,A__questionmark_yu83_49) ) ).

tff(formula_32,axiom,
    ! [A__questionmark_xu86_50: $real,A__questionmark_yu85_51: $real] :
      ( ( gt_real_bool(A__questionmark_xu86_50,A__questionmark_yu85_51) = c_Boolean_true )
    <=> $greater(A__questionmark_xu86_50,A__questionmark_yu85_51) ) ).

tff(formula_33,axiom,
    ! [A__questionmark_xu88_52: $real,A__questionmark_yu87_53: $real] :
      ( ( ge_real_bool(A__questionmark_xu88_52,A__questionmark_yu87_53) = c_Boolean_true )
    <=> $greatereq(A__questionmark_xu88_52,A__questionmark_yu87_53) ) ).

tff(formula_34,axiom,
    ! [A__questionmark_xu90_54: $real,A__questionmark_yu89_55: $real] :
      ( ( eq_real_bool(A__questionmark_xu90_54,A__questionmark_yu89_55) = c_Boolean_true )
    <=> ( A__questionmark_xu90_54 = A__questionmark_yu89_55 ) ) ).

tff(formula_35,axiom,
    ! [A__questionmark_xu92_56: $real,A__questionmark_yu91_57: $real] :
      ( ( neq_real_bool(A__questionmark_xu92_56,A__questionmark_yu91_57) = c_Boolean_true )
    <=> ( A__questionmark_xu92_56 != A__questionmark_yu91_57 ) ) ).

tff(formula_36,axiom,
    ! [A__questionmark_xu94_58: $real,A__questionmark_yu93_59: $real] :
    ? [A__questionmark_v_0_8: $real] :
      ( ( A__questionmark_v_0_8 = real_max(A__questionmark_xu94_58,A__questionmark_yu93_59) )
      & $greatereq(A__questionmark_v_0_8,A__questionmark_xu94_58)
      & $greatereq(A__questionmark_v_0_8,A__questionmark_yu93_59) ) ).

tff(formula_37,axiom,
    ! [A__questionmark_xu96_60: $real,A__questionmark_yu95_61: $real] :
    ? [A__questionmark_v_0_9: $real] :
      ( ( A__questionmark_v_0_9 = real_max(A__questionmark_xu96_60,A__questionmark_yu95_61) )
      & ( ( A__questionmark_v_0_9 = A__questionmark_xu96_60 )
        | ( A__questionmark_v_0_9 = A__questionmark_yu95_61 ) ) ) ).

tff(formula_38,axiom,
    ! [A__questionmark_xu98_62: $real,A__questionmark_yu97_63: $real] :
    ? [A__questionmark_v_0_10: $real] :
      ( ( A__questionmark_v_0_10 = real_min(A__questionmark_xu98_62,A__questionmark_yu97_63) )
      & $lesseq(A__questionmark_v_0_10,A__questionmark_xu98_62)
      & $lesseq(A__questionmark_v_0_10,A__questionmark_yu97_63) ) ).

tff(formula_39,axiom,
    ! [A__questionmark_xu100_64: $real,A__questionmark_yu99_65: $real] :
    ? [A__questionmark_v_0_11: $real] :
      ( ( A__questionmark_v_0_11 = real_min(A__questionmark_xu100_64,A__questionmark_yu99_65) )
      & ( ( A__questionmark_v_0_11 = A__questionmark_xu100_64 )
        | ( A__questionmark_v_0_11 = A__questionmark_yu99_65 ) ) ) ).

tff(formula_40,axiom,
    ! [A__questionmark_xu102_66: $real] :
      ( $greatereq(A__questionmark_xu102_66,0.0)
     => ( abs_real(A__questionmark_xu102_66) = A__questionmark_xu102_66 ) ) ).

tff(formula_41,axiom,
    ! [A__questionmark_xu103_67: $real] :
      ( $lesseq(A__questionmark_xu103_67,0.0)
     => ( abs_real(A__questionmark_xu103_67) = $uminus(A__questionmark_xu103_67) ) ) ).

tff(formula_42,axiom,
    ! [A__questionmark_xu104_68: $real] : ( log(exp(A__questionmark_xu104_68)) = A__questionmark_xu104_68 ) ).

tff(formula_43,axiom,
    ! [A__questionmark_t1u0_69: c_type,A__questionmark_au0_70: c_unsorted,A__questionmark_pu0_71: c_unsorted] :
    ? [A__questionmark_v_0_12: c_sorted,A__questionmark_v_1_13: c_sorted] :
      ( ( A__questionmark_v_0_12 = c_sort(alloc_table(A__questionmark_t1u0_69),A__questionmark_au0_70) )
      & ( A__questionmark_v_1_13 = c_sort(pointer(A__questionmark_t1u0_69),A__questionmark_pu0_71) )
      & ( valid(A__questionmark_v_0_12,A__questionmark_v_1_13)
      <=> ( $lesseq(offset_min(A__questionmark_v_0_12,A__questionmark_v_1_13),0)
          & $greatereq(offset_max(A__questionmark_v_0_12,A__questionmark_v_1_13),0) ) ) ) ).

tff(formula_44,axiom,
    ! [A__questionmark_t1u0_72: c_type,A__questionmark_pu0_73: c_unsorted,A__questionmark_qu0_74: c_unsorted] :
    ? [A__questionmark_v_0_14: c_type] :
      ( ( A__questionmark_v_0_14 = pointer(A__questionmark_t1u0_72) )
      & ? [A__questionmark_v_1_15: c_sorted,A__questionmark_v_3_16: c_sorted,A__questionmark_v_2_17: c_type] :
          ( ( A__questionmark_v_1_15 = c_sort(A__questionmark_v_0_14,A__questionmark_pu0_73) )
          & ( A__questionmark_v_3_16 = c_sort(A__questionmark_v_0_14,A__questionmark_qu0_74) )
          & ( A__questionmark_v_2_17 = block(A__questionmark_t1u0_72) )
          & ( same_block(A__questionmark_v_1_15,A__questionmark_v_3_16)
          <=> ( c_sort(A__questionmark_v_2_17,base_block(A__questionmark_v_1_15)) = c_sort(A__questionmark_v_2_17,base_block(A__questionmark_v_3_16)) ) ) ) ) ).

tff(formula_45,axiom,
    ! [A__questionmark_t1u0_75: c_type,A__questionmark_pu111_76: c_unsorted,A__questionmark_qu110_77: c_unsorted] :
    ? [A__questionmark_v_0_18: c_type] :
      ( ( A__questionmark_v_0_18 = pointer(A__questionmark_t1u0_75) )
      & ? [A__questionmark_v_1_19: c_sorted,A__questionmark_v_2_20: c_sorted] :
          ( ( A__questionmark_v_1_19 = c_sort(A__questionmark_v_0_18,A__questionmark_pu111_76) )
          & ( A__questionmark_v_2_20 = c_sort(A__questionmark_v_0_18,A__questionmark_qu110_77) )
          & ( ( A__questionmark_v_1_19 = A__questionmark_v_2_20 )
          <=> ( address(A__questionmark_v_1_19) = address(A__questionmark_v_2_20) ) ) ) ) ).

tff(formula_46,axiom,
    ! [A__questionmark_t1u0_78: c_type] : ( address(c_sort(pointer(A__questionmark_t1u0_78),null)) = 0 ) ).

tff(formula_47,axiom,
    ! [A__questionmark_t1u0_79: c_type,A__questionmark_pu112_80: c_unsorted] : $lesseq(0,address(c_sort(pointer(A__questionmark_t1u0_79),A__questionmark_pu112_80))) ).

tff(formula_48,axiom,
    ! [A__questionmark_t1u0_81: c_type,A__questionmark_pu115_82: c_unsorted,A__questionmark_iu114_83: $int,A__questionmark_ju113_84: $int] :
    ? [A__questionmark_v_0_21: c_type] :
      ( ( A__questionmark_v_0_21 = pointer(A__questionmark_t1u0_81) )
      & ? [A__questionmark_v_1_22: c_sorted] :
          ( ( A__questionmark_v_1_22 = c_sort(A__questionmark_v_0_21,A__questionmark_pu115_82) )
          & ( $less(address(c_sort(A__questionmark_v_0_21,shift(A__questionmark_v_1_22,A__questionmark_iu114_83))),address(c_sort(A__questionmark_v_0_21,shift(A__questionmark_v_1_22,A__questionmark_ju113_84))))
          <=> $less(A__questionmark_iu114_83,A__questionmark_ju113_84) ) ) ) ).

tff(formula_49,axiom,
    ! [A__questionmark_t1u0_85: c_type,A__questionmark_pu118_86: c_unsorted,A__questionmark_iu117_87: $int,A__questionmark_ju116_88: $int] :
    ? [A__questionmark_v_0_23: c_type] :
      ( ( A__questionmark_v_0_23 = pointer(A__questionmark_t1u0_85) )
      & ? [A__questionmark_v_1_24: c_sorted] :
          ( ( A__questionmark_v_1_24 = c_sort(A__questionmark_v_0_23,A__questionmark_pu118_86) )
          & ( $lesseq(address(c_sort(A__questionmark_v_0_23,shift(A__questionmark_v_1_24,A__questionmark_iu117_87))),address(c_sort(A__questionmark_v_0_23,shift(A__questionmark_v_1_24,A__questionmark_ju116_88))))
          <=> $lesseq(A__questionmark_iu117_87,A__questionmark_ju116_88) ) ) ) ).

tff(formula_50,axiom,
    ! [A__questionmark_t1u0_89: c_type,A__questionmark_pu119_90: c_unsorted] :
    ? [A__questionmark_v_0_25: c_type] :
      ( ( A__questionmark_v_0_25 = pointer(A__questionmark_t1u0_89) )
      & ? [A__questionmark_v_1_26: c_sorted] :
          ( ( A__questionmark_v_1_26 = c_sort(A__questionmark_v_0_25,A__questionmark_pu119_90) )
          & ( c_sort(A__questionmark_v_0_25,shift(A__questionmark_v_1_26,0)) = A__questionmark_v_1_26 ) ) ) ).

tff(formula_51,axiom,
    ! [A__questionmark_t1u0_91: c_type,A__questionmark_pu122_92: c_unsorted,A__questionmark_iu121_93: $int,A__questionmark_ju120_94: $int] :
    ? [A__questionmark_v_0_27: c_type] :
      ( ( A__questionmark_v_0_27 = pointer(A__questionmark_t1u0_91) )
      & ? [A__questionmark_v_1_28: c_sorted] :
          ( ( A__questionmark_v_1_28 = c_sort(A__questionmark_v_0_27,A__questionmark_pu122_92) )
          & ( c_sort(A__questionmark_v_0_27,shift(c_sort(A__questionmark_v_0_27,shift(A__questionmark_v_1_28,A__questionmark_iu121_93)),A__questionmark_ju120_94)) = c_sort(A__questionmark_v_0_27,shift(A__questionmark_v_1_28,$sum(A__questionmark_iu121_93,A__questionmark_ju120_94))) ) ) ) ).

tff(formula_52,axiom,
    ! [A__questionmark_t1u0_95: c_type,A__questionmark_au125_96: c_unsorted,A__questionmark_pu124_97: c_unsorted,A__questionmark_iu123_98: $int] :
    ? [A__questionmark_v_1_29: c_sorted,A__questionmark_v_0_30: c_type] :
      ( ( A__questionmark_v_1_29 = c_sort(alloc_table(A__questionmark_t1u0_95),A__questionmark_au125_96) )
      & ( A__questionmark_v_0_30 = pointer(A__questionmark_t1u0_95) )
      & ? [A__questionmark_v_2_31: c_sorted] :
          ( ( A__questionmark_v_2_31 = c_sort(A__questionmark_v_0_30,A__questionmark_pu124_97) )
          & ( offset_max(A__questionmark_v_1_29,c_sort(A__questionmark_v_0_30,shift(A__questionmark_v_2_31,A__questionmark_iu123_98))) = $difference(offset_max(A__questionmark_v_1_29,A__questionmark_v_2_31),A__questionmark_iu123_98) ) ) ) ).

tff(formula_53,axiom,
    ! [A__questionmark_t1u0_99: c_type,A__questionmark_au128_100: c_unsorted,A__questionmark_pu127_101: c_unsorted,A__questionmark_iu126_102: $int] :
    ? [A__questionmark_v_1_32: c_sorted,A__questionmark_v_0_33: c_type] :
      ( ( A__questionmark_v_1_32 = c_sort(alloc_table(A__questionmark_t1u0_99),A__questionmark_au128_100) )
      & ( A__questionmark_v_0_33 = pointer(A__questionmark_t1u0_99) )
      & ? [A__questionmark_v_2_34: c_sorted] :
          ( ( A__questionmark_v_2_34 = c_sort(A__questionmark_v_0_33,A__questionmark_pu127_101) )
          & ( offset_min(A__questionmark_v_1_32,c_sort(A__questionmark_v_0_33,shift(A__questionmark_v_2_34,A__questionmark_iu126_102))) = $difference(offset_min(A__questionmark_v_1_32,A__questionmark_v_2_34),A__questionmark_iu126_102) ) ) ) ).

tff(formula_54,axiom,
    ! [A__questionmark_t1u0_103: c_type,A__questionmark_pu131_104: c_unsorted,A__questionmark_iu130_105: $int,A__questionmark_ju129_106: $int] :
    ? [A__questionmark_v_0_35: c_type] :
      ( ( A__questionmark_v_0_35 = pointer(A__questionmark_t1u0_103) )
      & ? [A__questionmark_v_1_36: c_sorted] :
          ( ( A__questionmark_v_1_36 = c_sort(A__questionmark_v_0_35,A__questionmark_pu131_104) )
          & ( ( A__questionmark_iu130_105 != A__questionmark_ju129_106 )
           => ( c_sort(A__questionmark_v_0_35,shift(A__questionmark_v_1_36,A__questionmark_iu130_105)) != c_sort(A__questionmark_v_0_35,shift(A__questionmark_v_1_36,A__questionmark_ju129_106)) ) ) ) ) ).

tff(formula_55,axiom,
    ! [A__questionmark_t1u0_107: c_type,A__questionmark_au132_108: c_unsorted] : ~ valid(c_sort(alloc_table(A__questionmark_t1u0_107),A__questionmark_au132_108),c_sort(pointer(A__questionmark_t1u0_107),null)) ).

tff(formula_56,axiom,
    ! [A__questionmark_t1u0_109: c_type,A__questionmark_au133_110: c_unsorted] :
    ? [A__questionmark_v_0_37: c_sorted,A__questionmark_v_1_38: c_sorted] :
      ( ( A__questionmark_v_0_37 = c_sort(alloc_table(A__questionmark_t1u0_109),A__questionmark_au133_110) )
      & ( A__questionmark_v_1_38 = c_sort(pointer(A__questionmark_t1u0_109),null) )
      & $greatereq(offset_min(A__questionmark_v_0_37,A__questionmark_v_1_38),0)
      & $lesseq(offset_max(A__questionmark_v_0_37,A__questionmark_v_1_38),$uminus(2)) ) ).

tff(formula_57,axiom,
    ! [A__questionmark_t1u0_111: c_type,A__questionmark_p1u143_112: c_unsorted,A__questionmark_p2u142_113: c_unsorted] :
    ? [A__questionmark_v_0_39: c_type] :
      ( ( A__questionmark_v_0_39 = pointer(A__questionmark_t1u0_111) )
      & ? [A__questionmark_v_1_40: c_sorted,A__questionmark_v_2_41: c_sorted] :
          ( ( A__questionmark_v_1_40 = c_sort(A__questionmark_v_0_39,A__questionmark_p1u143_112) )
          & ( A__questionmark_v_2_41 = c_sort(A__questionmark_v_0_39,A__questionmark_p2u142_113) )
          & ( ( eq_pointer_bool(A__questionmark_v_1_40,A__questionmark_v_2_41) = c_Boolean_true )
          <=> ( A__questionmark_v_1_40 = A__questionmark_v_2_41 ) ) ) ) ).

tff(formula_58,axiom,
    ! [A__questionmark_t1u0_114: c_type,A__questionmark_p1u145_115: c_unsorted,A__questionmark_p2u144_116: c_unsorted] :
    ? [A__questionmark_v_0_42: c_type] :
      ( ( A__questionmark_v_0_42 = pointer(A__questionmark_t1u0_114) )
      & ? [A__questionmark_v_1_43: c_sorted,A__questionmark_v_2_44: c_sorted] :
          ( ( A__questionmark_v_1_43 = c_sort(A__questionmark_v_0_42,A__questionmark_p1u145_115) )
          & ( A__questionmark_v_2_44 = c_sort(A__questionmark_v_0_42,A__questionmark_p2u144_116) )
          & ( ( neq_pointer_bool(A__questionmark_v_1_43,A__questionmark_v_2_44) = c_Boolean_true )
          <=> ( A__questionmark_v_1_43 != A__questionmark_v_2_44 ) ) ) ) ).

tff(formula_59,axiom,
    ! [A__questionmark_t1u0_117: c_type,A__questionmark_pu148_118: c_unsorted,A__questionmark_qu147_119: c_unsorted,A__questionmark_iu146_120: $int] :
    ? [A__questionmark_v_0_45: c_type] :
      ( ( A__questionmark_v_0_45 = pointer(A__questionmark_t1u0_117) )
      & ? [A__questionmark_v_1_46: c_sorted,A__questionmark_v_2_47: c_sorted] :
          ( ( A__questionmark_v_1_46 = c_sort(A__questionmark_v_0_45,A__questionmark_pu148_118) )
          & ( A__questionmark_v_2_47 = c_sort(A__questionmark_v_0_45,A__questionmark_qu147_119) )
          & ( same_block(A__questionmark_v_1_46,A__questionmark_v_2_47)
           => same_block(A__questionmark_v_1_46,c_sort(A__questionmark_v_0_45,shift(A__questionmark_v_2_47,A__questionmark_iu146_120))) ) ) ) ).

tff(formula_60,axiom,
    ! [A__questionmark_t1u0_121: c_type,A__questionmark_pu151_122: c_unsorted,A__questionmark_qu150_123: c_unsorted,A__questionmark_iu149_124: $int] :
    ? [A__questionmark_v_0_48: c_type] :
      ( ( A__questionmark_v_0_48 = pointer(A__questionmark_t1u0_121) )
      & ? [A__questionmark_v_1_49: c_sorted,A__questionmark_v_2_50: c_sorted] :
          ( ( A__questionmark_v_1_49 = c_sort(A__questionmark_v_0_48,A__questionmark_qu150_123) )
          & ( A__questionmark_v_2_50 = c_sort(A__questionmark_v_0_48,A__questionmark_pu151_122) )
          & ( same_block(A__questionmark_v_1_49,A__questionmark_v_2_50)
           => same_block(c_sort(A__questionmark_v_0_48,shift(A__questionmark_v_1_49,A__questionmark_iu149_124)),A__questionmark_v_2_50) ) ) ) ).

tff(formula_61,axiom,
    ! [A__questionmark_t1u0_125: c_type,A__questionmark_pu153_126: c_unsorted,A__questionmark_qu152_127: c_unsorted] :
    ? [A__questionmark_v_0_51: c_type] :
      ( ( A__questionmark_v_0_51 = pointer(A__questionmark_t1u0_125) )
      & ? [A__questionmark_v_1_52: c_sorted,A__questionmark_v_2_53: c_sorted] :
          ( ( A__questionmark_v_1_52 = c_sort(A__questionmark_v_0_51,A__questionmark_pu153_126) )
          & ( A__questionmark_v_2_53 = c_sort(A__questionmark_v_0_51,A__questionmark_qu152_127) )
          & ( same_block(A__questionmark_v_1_52,A__questionmark_v_2_53)
           => ( A__questionmark_v_1_52 = c_sort(A__questionmark_v_0_51,shift(A__questionmark_v_2_53,sub_pointer(A__questionmark_v_1_52,A__questionmark_v_2_53))) ) ) ) ) ).

tff(formula_62,axiom,
    ! [A__questionmark_t1u0_128: c_type,A__questionmark_pu154_129: c_unsorted] :
    ? [A__questionmark_v_0_54: c_sorted] :
      ( ( A__questionmark_v_0_54 = c_sort(pointer(A__questionmark_t1u0_128),A__questionmark_pu154_129) )
      & ( sub_pointer(A__questionmark_v_0_54,A__questionmark_v_0_54) = 0 ) ) ).

tff(formula_63,axiom,
    ! [A__questionmark_t1u0_130: c_type,A__questionmark_pu156_131: c_unsorted,A__questionmark_qu155_132: c_unsorted] :
    ? [A__questionmark_v_0_55: c_type] :
      ( ( A__questionmark_v_0_55 = pointer(A__questionmark_t1u0_130) )
      & ? [A__questionmark_v_1_56: c_sorted,A__questionmark_v_2_57: c_sorted] :
          ( ( A__questionmark_v_1_56 = c_sort(A__questionmark_v_0_55,A__questionmark_pu156_131) )
          & ( A__questionmark_v_2_57 = c_sort(A__questionmark_v_0_55,A__questionmark_qu155_132) )
          & ( same_block(A__questionmark_v_1_56,A__questionmark_v_2_57)
           => ( ( sub_pointer(A__questionmark_v_1_56,A__questionmark_v_2_57) = 0 )
             => ( A__questionmark_v_1_56 = A__questionmark_v_2_57 ) ) ) ) ) ).

tff(formula_64,axiom,
    ! [A__questionmark_t1u0_133: c_type,A__questionmark_pu159_134: c_unsorted,A__questionmark_qu158_135: c_unsorted,A__questionmark_iu157_136: $int] :
    ? [A__questionmark_v_0_58: c_type] :
      ( ( A__questionmark_v_0_58 = pointer(A__questionmark_t1u0_133) )
      & ? [A__questionmark_v_1_59: c_sorted,A__questionmark_v_2_60: c_sorted] :
          ( ( A__questionmark_v_1_59 = c_sort(A__questionmark_v_0_58,A__questionmark_pu159_134) )
          & ( A__questionmark_v_2_60 = c_sort(A__questionmark_v_0_58,A__questionmark_qu158_135) )
          & ( sub_pointer(c_sort(A__questionmark_v_0_58,shift(A__questionmark_v_1_59,A__questionmark_iu157_136)),A__questionmark_v_2_60) = $sum(sub_pointer(A__questionmark_v_1_59,A__questionmark_v_2_60),A__questionmark_iu157_136) ) ) ) ).

tff(formula_65,axiom,
    ! [A__questionmark_t1u0_137: c_type,A__questionmark_pu162_138: c_unsorted,A__questionmark_qu161_139: c_unsorted,A__questionmark_iu160_140: $int] :
    ? [A__questionmark_v_0_61: c_type] :
      ( ( A__questionmark_v_0_61 = pointer(A__questionmark_t1u0_137) )
      & ? [A__questionmark_v_1_62: c_sorted,A__questionmark_v_2_63: c_sorted] :
          ( ( A__questionmark_v_1_62 = c_sort(A__questionmark_v_0_61,A__questionmark_pu162_138) )
          & ( A__questionmark_v_2_63 = c_sort(A__questionmark_v_0_61,A__questionmark_qu161_139) )
          & ( sub_pointer(A__questionmark_v_1_62,c_sort(A__questionmark_v_0_61,shift(A__questionmark_v_2_63,A__questionmark_iu160_140))) = $difference(sub_pointer(A__questionmark_v_1_62,A__questionmark_v_2_63),A__questionmark_iu160_140) ) ) ) ).

tff(formula_66,axiom,
    ! [A__questionmark_t2u0_141: c_type,A__questionmark_t1u0_142: c_type,A__questionmark_mu166_143: c_unsorted,A__questionmark_p1u165_144: c_unsorted,A__questionmark_p2u164_145: c_unsorted,A__questionmark_au163_146: c_unsorted] :
    ? [A__questionmark_v_0_64: c_type] :
      ( ( A__questionmark_v_0_64 = pointer(A__questionmark_t1u0_142) )
      & ? [A__questionmark_v_2_65: c_sorted,A__questionmark_v_3_66: c_sorted,A__questionmark_v_1_67: c_type,A__questionmark_v_4_68: c_sorted] :
          ( ( A__questionmark_v_2_65 = c_sort(A__questionmark_v_0_64,A__questionmark_p1u165_144) )
          & ( A__questionmark_v_3_66 = c_sort(A__questionmark_v_0_64,A__questionmark_p2u164_145) )
          & ( A__questionmark_v_1_67 = memory(A__questionmark_t1u0_142,A__questionmark_t2u0_141) )
          & ( A__questionmark_v_4_68 = c_sort(A__questionmark_t2u0_141,A__questionmark_au163_146) )
          & ( ( A__questionmark_v_2_65 = A__questionmark_v_3_66 )
           => ( c_sort(A__questionmark_t2u0_141,smtlib__select(c_sort(A__questionmark_v_1_67,smtlib__store(c_sort(A__questionmark_v_1_67,A__questionmark_mu166_143),A__questionmark_v_2_65,A__questionmark_v_4_68)),A__questionmark_v_3_66)) = A__questionmark_v_4_68 ) ) ) ) ).

tff(formula_67,axiom,
    ! [A__questionmark_t2u0_147: c_type,A__questionmark_t1u0_148: c_type,A__questionmark_mu170_149: c_unsorted,A__questionmark_p1u169_150: c_unsorted,A__questionmark_p2u168_151: c_unsorted,A__questionmark_au167_152: c_unsorted] :
    ? [A__questionmark_v_0_69: c_type] :
      ( ( A__questionmark_v_0_69 = pointer(A__questionmark_t1u0_148) )
      & ? [A__questionmark_v_2_70: c_sorted,A__questionmark_v_3_71: c_sorted,A__questionmark_v_1_72: c_type] :
          ( ( A__questionmark_v_2_70 = c_sort(A__questionmark_v_0_69,A__questionmark_p1u169_150) )
          & ( A__questionmark_v_3_71 = c_sort(A__questionmark_v_0_69,A__questionmark_p2u168_151) )
          & ( A__questionmark_v_1_72 = memory(A__questionmark_t1u0_148,A__questionmark_t2u0_147) )
          & ? [A__questionmark_v_4_73: c_sorted] :
              ( ( A__questionmark_v_4_73 = c_sort(A__questionmark_v_1_72,A__questionmark_mu170_149) )
              & ( ( A__questionmark_v_2_70 != A__questionmark_v_3_71 )
               => ( c_sort(A__questionmark_t2u0_147,smtlib__select(c_sort(A__questionmark_v_1_72,smtlib__store(A__questionmark_v_4_73,A__questionmark_v_2_70,c_sort(A__questionmark_t2u0_147,A__questionmark_au167_152))),A__questionmark_v_3_71)) = c_sort(A__questionmark_t2u0_147,smtlib__select(A__questionmark_v_4_73,A__questionmark_v_3_71)) ) ) ) ) ) ).

tff(formula_68,axiom,
    ! [A__questionmark_t1u0_153: c_type,A__questionmark_ps1u0_154: c_unsorted,A__questionmark_ps2u0_155: c_unsorted] :
    ? [A__questionmark_v_0_74: c_type] :
      ( ( A__questionmark_v_0_74 = pset(A__questionmark_t1u0_153) )
      & ( pset_disjoint(c_sort(A__questionmark_v_0_74,A__questionmark_ps1u0_154),c_sort(A__questionmark_v_0_74,A__questionmark_ps2u0_155))
      <=> ! [A__questionmark_pu261_156: c_unsorted] :
          ? [A__questionmark_v_1_75: c_sorted] :
            ( ( A__questionmark_v_1_75 = c_sort(pointer(A__questionmark_t1u0_153),A__questionmark_pu261_156) )
            & ~ ( in_pset(A__questionmark_v_1_75,c_sort(A__questionmark_v_0_74,A__questionmark_ps1u0_154))
                & in_pset(A__questionmark_v_1_75,c_sort(A__questionmark_v_0_74,A__questionmark_ps2u0_155)) ) ) ) ) ).

tff(formula_69,axiom,
    ! [A__questionmark_t1u0_157: c_type,A__questionmark_ps1u0_158: c_unsorted,A__questionmark_ps2u0_159: c_unsorted] :
    ? [A__questionmark_v_0_76: c_type] :
      ( ( A__questionmark_v_0_76 = pset(A__questionmark_t1u0_157) )
      & ( pset_included(c_sort(A__questionmark_v_0_76,A__questionmark_ps1u0_158),c_sort(A__questionmark_v_0_76,A__questionmark_ps2u0_159))
      <=> ! [A__questionmark_pu262_160: c_unsorted] :
          ? [A__questionmark_v_1_77: c_sorted] :
            ( ( A__questionmark_v_1_77 = c_sort(pointer(A__questionmark_t1u0_157),A__questionmark_pu262_160) )
            & ( in_pset(A__questionmark_v_1_77,c_sort(A__questionmark_v_0_76,A__questionmark_ps1u0_158))
             => in_pset(A__questionmark_v_1_77,c_sort(A__questionmark_v_0_76,A__questionmark_ps2u0_159)) ) ) ) ) ).

tff(formula_70,axiom,
    ! [A__questionmark_t1u0_161: c_type,A__questionmark_psu263_162: c_unsorted] :
    ? [A__questionmark_v_0_78: c_sorted] :
      ( ( A__questionmark_v_0_78 = c_sort(pset(A__questionmark_t1u0_161),A__questionmark_psu263_162) )
      & pset_included(A__questionmark_v_0_78,A__questionmark_v_0_78) ) ).

tff(formula_71,axiom,
    ! [A__questionmark_t1u0_163: c_type,A__questionmark_psu268_164: c_unsorted,A__questionmark_au267_165: $int,A__questionmark_bu266_166: $int,A__questionmark_cu265_167: $int,A__questionmark_du264_168: $int] :
    ? [A__questionmark_v_0_79: c_type] :
      ( ( A__questionmark_v_0_79 = pset(A__questionmark_t1u0_163) )
      & ? [A__questionmark_v_1_80: c_sorted] :
          ( ( A__questionmark_v_1_80 = c_sort(A__questionmark_v_0_79,A__questionmark_psu268_164) )
          & ( ( $lesseq(A__questionmark_cu265_167,A__questionmark_au267_165)
              & $lesseq(A__questionmark_bu266_166,A__questionmark_du264_168) )
           => pset_included(c_sort(A__questionmark_v_0_79,pset_range(A__questionmark_v_1_80,A__questionmark_au267_165,A__questionmark_bu266_166)),c_sort(A__questionmark_v_0_79,pset_range(A__questionmark_v_1_80,A__questionmark_cu265_167,A__questionmark_du264_168))) ) ) ) ).

tff(formula_72,axiom,
    ! [A__questionmark_t1u0_169: c_type,A__questionmark_psu273_170: c_unsorted,A__questionmark_au272_171: $int,A__questionmark_bu271_172: $int,A__questionmark_cu270_173: $int,A__questionmark_du269_174: $int] :
    ? [A__questionmark_v_0_81: c_type] :
      ( ( A__questionmark_v_0_81 = pset(A__questionmark_t1u0_169) )
      & ? [A__questionmark_v_1_82: c_sorted] :
          ( ( A__questionmark_v_1_82 = c_sort(A__questionmark_v_0_81,A__questionmark_psu273_170) )
          & pset_included(c_sort(A__questionmark_v_0_81,pset_range(A__questionmark_v_1_82,A__questionmark_au272_171,A__questionmark_bu271_172)),c_sort(A__questionmark_v_0_81,pset_all(A__questionmark_v_1_82))) ) ) ).

tff(formula_73,axiom,
    ! [A__questionmark_t1u0_175: c_type,A__questionmark_pu274_176: c_unsorted] : ~ in_pset(c_sort(pointer(A__questionmark_t1u0_175),A__questionmark_pu274_176),c_sort(pset(A__questionmark_t1u0_175),pset_empty)) ).

tff(formula_74,axiom,
    ! [A__questionmark_t1u0_177: c_type,A__questionmark_pu276_178: c_unsorted,A__questionmark_qu275_179: c_unsorted] :
    ? [A__questionmark_v_0_83: c_type] :
      ( ( A__questionmark_v_0_83 = pointer(A__questionmark_t1u0_177) )
      & ? [A__questionmark_v_1_84: c_sorted,A__questionmark_v_2_85: c_sorted] :
          ( ( A__questionmark_v_1_84 = c_sort(A__questionmark_v_0_83,A__questionmark_pu276_178) )
          & ( A__questionmark_v_2_85 = c_sort(A__questionmark_v_0_83,A__questionmark_qu275_179) )
          & ( in_pset(A__questionmark_v_1_84,c_sort(pset(A__questionmark_t1u0_177),pset_singleton(A__questionmark_v_2_85)))
          <=> ( A__questionmark_v_1_84 = A__questionmark_v_2_85 ) ) ) ) ).

tff(formula_75,axiom,
    ! [A__questionmark_t2u0_180: c_type,A__questionmark_t1u0_181: c_type,A__questionmark_pu280_182: c_unsorted,A__questionmark_mu279_183: c_unsorted,A__questionmark_qu278_184: c_unsorted] :
    ? [A__questionmark_v_0_86: c_type] :
      ( ( A__questionmark_v_0_86 = pointer(A__questionmark_t1u0_181) )
      & ( in_pset(c_sort(A__questionmark_v_0_86,A__questionmark_pu280_182),c_sort(pset(A__questionmark_t1u0_181),pset_deref(c_sort(memory(A__questionmark_t2u0_180,A__questionmark_v_0_86),A__questionmark_mu279_183),c_sort(pset(A__questionmark_t2u0_180),A__questionmark_qu278_184))))
      <=> ? [A__questionmark_ru277_185: c_unsorted,A__questionmark_v_1_87: c_sorted] :
            ( ( A__questionmark_v_1_87 = c_sort(pointer(A__questionmark_t2u0_180),A__questionmark_ru277_185) )
            & in_pset(A__questionmark_v_1_87,c_sort(pset(A__questionmark_t2u0_180),A__questionmark_qu278_184))
            & ( c_sort(A__questionmark_v_0_86,A__questionmark_pu280_182) = c_sort(A__questionmark_v_0_86,smtlib__select(c_sort(memory(A__questionmark_t2u0_180,A__questionmark_v_0_86),A__questionmark_mu279_183),A__questionmark_v_1_87)) ) ) ) ) ).

tff(formula_76,axiom,
    ! [A__questionmark_t1u0_186: c_type,A__questionmark_pu284_187: c_unsorted,A__questionmark_qu283_188: c_unsorted] :
    ? [A__questionmark_v_0_88: c_type] :
      ( ( A__questionmark_v_0_88 = pset(A__questionmark_t1u0_186) )
      & ( in_pset(c_sort(pointer(A__questionmark_t1u0_186),A__questionmark_pu284_187),c_sort(A__questionmark_v_0_88,pset_all(c_sort(A__questionmark_v_0_88,A__questionmark_qu283_188))))
      <=> ? [A__questionmark_iu282_189: $int,A__questionmark_ru281_190: c_unsorted,A__questionmark_v_1_89: c_type] :
            ( ( A__questionmark_v_1_89 = pointer(A__questionmark_t1u0_186) )
            & ? [A__questionmark_v_2_90: c_sorted] :
                ( ( A__questionmark_v_2_90 = c_sort(A__questionmark_v_1_89,A__questionmark_ru281_190) )
                & in_pset(A__questionmark_v_2_90,c_sort(A__questionmark_v_0_88,A__questionmark_qu283_188))
                & ( c_sort(A__questionmark_v_1_89,A__questionmark_pu284_187) = c_sort(A__questionmark_v_1_89,shift(A__questionmark_v_2_90,A__questionmark_iu282_189)) ) ) ) ) ) ).

tff(formula_77,axiom,
    ! [A__questionmark_t1u0_191: c_type,A__questionmark_pu290_192: c_unsorted,A__questionmark_qu289_193: c_unsorted,A__questionmark_au288_194: $int,A__questionmark_bu287_195: $int] :
    ? [A__questionmark_v_0_91: c_type] :
      ( ( A__questionmark_v_0_91 = pset(A__questionmark_t1u0_191) )
      & ( in_pset(c_sort(pointer(A__questionmark_t1u0_191),A__questionmark_pu290_192),c_sort(A__questionmark_v_0_91,pset_range(c_sort(A__questionmark_v_0_91,A__questionmark_qu289_193),A__questionmark_au288_194,A__questionmark_bu287_195)))
      <=> ? [A__questionmark_iu286_196: $int,A__questionmark_ru285_197: c_unsorted,A__questionmark_v_1_92: c_type] :
            ( ( A__questionmark_v_1_92 = pointer(A__questionmark_t1u0_191) )
            & ? [A__questionmark_v_2_93: c_sorted] :
                ( ( A__questionmark_v_2_93 = c_sort(A__questionmark_v_1_92,A__questionmark_ru285_197) )
                & $lesseq(A__questionmark_au288_194,A__questionmark_iu286_196)
                & $lesseq(A__questionmark_iu286_196,A__questionmark_bu287_195)
                & in_pset(A__questionmark_v_2_93,c_sort(A__questionmark_v_0_91,A__questionmark_qu289_193))
                & ( c_sort(A__questionmark_v_1_92,A__questionmark_pu290_192) = c_sort(A__questionmark_v_1_92,shift(A__questionmark_v_2_93,A__questionmark_iu286_196)) ) ) ) ) ) ).

tff(formula_78,axiom,
    ! [A__questionmark_t1u0_198: c_type,A__questionmark_pu295_199: c_unsorted,A__questionmark_qu294_200: c_unsorted,A__questionmark_bu293_201: $int] :
    ? [A__questionmark_v_0_94: c_type] :
      ( ( A__questionmark_v_0_94 = pset(A__questionmark_t1u0_198) )
      & ( in_pset(c_sort(pointer(A__questionmark_t1u0_198),A__questionmark_pu295_199),c_sort(A__questionmark_v_0_94,pset_range_left(c_sort(A__questionmark_v_0_94,A__questionmark_qu294_200),A__questionmark_bu293_201)))
      <=> ? [A__questionmark_iu292_202: $int,A__questionmark_ru291_203: c_unsorted,A__questionmark_v_1_95: c_type] :
            ( ( A__questionmark_v_1_95 = pointer(A__questionmark_t1u0_198) )
            & ? [A__questionmark_v_2_96: c_sorted] :
                ( ( A__questionmark_v_2_96 = c_sort(A__questionmark_v_1_95,A__questionmark_ru291_203) )
                & $lesseq(A__questionmark_iu292_202,A__questionmark_bu293_201)
                & in_pset(A__questionmark_v_2_96,c_sort(A__questionmark_v_0_94,A__questionmark_qu294_200))
                & ( c_sort(A__questionmark_v_1_95,A__questionmark_pu295_199) = c_sort(A__questionmark_v_1_95,shift(A__questionmark_v_2_96,A__questionmark_iu292_202)) ) ) ) ) ) ).

tff(formula_79,axiom,
    ! [A__questionmark_t1u0_204: c_type,A__questionmark_pu300_205: c_unsorted,A__questionmark_qu299_206: c_unsorted,A__questionmark_au298_207: $int] :
    ? [A__questionmark_v_0_97: c_type] :
      ( ( A__questionmark_v_0_97 = pset(A__questionmark_t1u0_204) )
      & ( in_pset(c_sort(pointer(A__questionmark_t1u0_204),A__questionmark_pu300_205),c_sort(A__questionmark_v_0_97,pset_range_right(c_sort(A__questionmark_v_0_97,A__questionmark_qu299_206),A__questionmark_au298_207)))
      <=> ? [A__questionmark_iu297_208: $int,A__questionmark_ru296_209: c_unsorted,A__questionmark_v_1_98: c_type] :
            ( ( A__questionmark_v_1_98 = pointer(A__questionmark_t1u0_204) )
            & ? [A__questionmark_v_2_99: c_sorted] :
                ( ( A__questionmark_v_2_99 = c_sort(A__questionmark_v_1_98,A__questionmark_ru296_209) )
                & $lesseq(A__questionmark_au298_207,A__questionmark_iu297_208)
                & in_pset(A__questionmark_v_2_99,c_sort(A__questionmark_v_0_97,A__questionmark_qu299_206))
                & ( c_sort(A__questionmark_v_1_98,A__questionmark_pu300_205) = c_sort(A__questionmark_v_1_98,shift(A__questionmark_v_2_99,A__questionmark_iu297_208)) ) ) ) ) ) ).

tff(formula_80,axiom,
    ! [A__questionmark_t1u0_210: c_type,A__questionmark_pu303_211: c_unsorted,A__questionmark_s1u302_212: c_unsorted,A__questionmark_s2u301_213: c_unsorted] :
    ? [A__questionmark_v_1_100: c_sorted,A__questionmark_v_0_101: c_type] :
      ( ( A__questionmark_v_1_100 = c_sort(pointer(A__questionmark_t1u0_210),A__questionmark_pu303_211) )
      & ( A__questionmark_v_0_101 = pset(A__questionmark_t1u0_210) )
      & ? [A__questionmark_v_2_102: c_sorted,A__questionmark_v_3_103: c_sorted] :
          ( ( A__questionmark_v_2_102 = c_sort(A__questionmark_v_0_101,A__questionmark_s1u302_212) )
          & ( A__questionmark_v_3_103 = c_sort(A__questionmark_v_0_101,A__questionmark_s2u301_213) )
          & ( in_pset(A__questionmark_v_1_100,c_sort(A__questionmark_v_0_101,pset_union(A__questionmark_v_2_102,A__questionmark_v_3_103)))
          <=> ( in_pset(A__questionmark_v_1_100,A__questionmark_v_2_102)
              | in_pset(A__questionmark_v_1_100,A__questionmark_v_3_103) ) ) ) ) ).

tff(formula_81,axiom,
    ! [A__questionmark_t1u0_214: c_type,A__questionmark_au304_215: c_unsorted] : valid_pset(c_sort(alloc_table(A__questionmark_t1u0_214),A__questionmark_au304_215),c_sort(pset(A__questionmark_t1u0_214),pset_empty)) ).

tff(formula_82,axiom,
    ! [A__questionmark_t1u0_216: c_type,A__questionmark_au306_217: c_unsorted,A__questionmark_pu305_218: c_unsorted] :
    ? [A__questionmark_v_0_104: c_sorted,A__questionmark_v_1_105: c_sorted] :
      ( ( A__questionmark_v_0_104 = c_sort(alloc_table(A__questionmark_t1u0_216),A__questionmark_au306_217) )
      & ( A__questionmark_v_1_105 = c_sort(pointer(A__questionmark_t1u0_216),A__questionmark_pu305_218) )
      & ( valid_pset(A__questionmark_v_0_104,c_sort(pset(A__questionmark_t1u0_216),pset_singleton(A__questionmark_v_1_105)))
      <=> valid(A__questionmark_v_0_104,A__questionmark_v_1_105) ) ) ).

tff(formula_83,axiom,
    ! [A__questionmark_t2u0_219: c_type,A__questionmark_t1u0_220: c_type,A__questionmark_au311_221: c_unsorted,A__questionmark_mu310_222: c_unsorted,A__questionmark_qu309_223: c_unsorted] :
      ( valid_pset(c_sort(alloc_table(A__questionmark_t1u0_220),A__questionmark_au311_221),c_sort(pset(A__questionmark_t1u0_220),pset_deref(c_sort(memory(A__questionmark_t2u0_219,pointer(A__questionmark_t1u0_220)),A__questionmark_mu310_222),c_sort(pset(A__questionmark_t2u0_219),A__questionmark_qu309_223))))
    <=> ! [A__questionmark_ru308_224: c_unsorted,A__questionmark_pu307_225: c_unsorted] :
        ? [A__questionmark_v_0_106: c_type,A__questionmark_v_1_107: c_sorted] :
          ( ( A__questionmark_v_0_106 = pointer(A__questionmark_t1u0_220) )
          & ( A__questionmark_v_1_107 = c_sort(pointer(A__questionmark_t2u0_219),A__questionmark_ru308_224) )
          & ? [A__questionmark_v_2_108: c_sorted] :
              ( ( A__questionmark_v_2_108 = c_sort(A__questionmark_v_0_106,A__questionmark_pu307_225) )
              & ( ( in_pset(A__questionmark_v_1_107,c_sort(pset(A__questionmark_t2u0_219),A__questionmark_qu309_223))
                  & ( A__questionmark_v_2_108 = c_sort(A__questionmark_v_0_106,smtlib__select(c_sort(memory(A__questionmark_t2u0_219,A__questionmark_v_0_106),A__questionmark_mu310_222),A__questionmark_v_1_107)) ) )
               => valid(c_sort(alloc_table(A__questionmark_t1u0_220),A__questionmark_au311_221),A__questionmark_v_2_108) ) ) ) ) ).

tff(formula_84,axiom,
    ! [A__questionmark_t1u0_226: c_type,A__questionmark_au317_227: c_unsorted,A__questionmark_qu316_228: c_unsorted,A__questionmark_cu315_229: $int,A__questionmark_du314_230: $int] :
    ? [A__questionmark_v_0_109: c_type] :
      ( ( A__questionmark_v_0_109 = pset(A__questionmark_t1u0_226) )
      & ( valid_pset(c_sort(alloc_table(A__questionmark_t1u0_226),A__questionmark_au317_227),c_sort(A__questionmark_v_0_109,pset_range(c_sort(A__questionmark_v_0_109,A__questionmark_qu316_228),A__questionmark_cu315_229,A__questionmark_du314_230)))
      <=> ! [A__questionmark_iu313_231: $int,A__questionmark_ru312_232: c_unsorted] :
          ? [A__questionmark_v_1_110: c_type] :
            ( ( A__questionmark_v_1_110 = pointer(A__questionmark_t1u0_226) )
            & ? [A__questionmark_v_2_111: c_sorted] :
                ( ( A__questionmark_v_2_111 = c_sort(A__questionmark_v_1_110,A__questionmark_ru312_232) )
                & ( ( in_pset(A__questionmark_v_2_111,c_sort(A__questionmark_v_0_109,A__questionmark_qu316_228))
                    & $lesseq(A__questionmark_cu315_229,A__questionmark_iu313_231)
                    & $lesseq(A__questionmark_iu313_231,A__questionmark_du314_230) )
                 => valid(c_sort(alloc_table(A__questionmark_t1u0_226),A__questionmark_au317_227),c_sort(A__questionmark_v_1_110,shift(A__questionmark_v_2_111,A__questionmark_iu313_231))) ) ) ) ) ) ).

tff(formula_85,axiom,
    ! [A__questionmark_t1u0_233: c_type,A__questionmark_au320_234: c_unsorted,A__questionmark_s1u319_235: c_unsorted,A__questionmark_s2u318_236: c_unsorted] :
    ? [A__questionmark_v_1_112: c_sorted,A__questionmark_v_0_113: c_type] :
      ( ( A__questionmark_v_1_112 = c_sort(alloc_table(A__questionmark_t1u0_233),A__questionmark_au320_234) )
      & ( A__questionmark_v_0_113 = pset(A__questionmark_t1u0_233) )
      & ? [A__questionmark_v_2_114: c_sorted,A__questionmark_v_3_115: c_sorted] :
          ( ( A__questionmark_v_2_114 = c_sort(A__questionmark_v_0_113,A__questionmark_s1u319_235) )
          & ( A__questionmark_v_3_115 = c_sort(A__questionmark_v_0_113,A__questionmark_s2u318_236) )
          & ( valid_pset(A__questionmark_v_1_112,c_sort(A__questionmark_v_0_113,pset_union(A__questionmark_v_2_114,A__questionmark_v_3_115)))
          <=> ( valid_pset(A__questionmark_v_1_112,A__questionmark_v_2_114)
              & valid_pset(A__questionmark_v_1_112,A__questionmark_v_3_115) ) ) ) ) ).

tff(formula_86,axiom,
    ! [A__questionmark_t2u0_237: c_type,A__questionmark_t1u0_238: c_type,A__questionmark_au0_239: c_unsorted,A__questionmark_m1u0_240: c_unsorted,A__questionmark_m2u0_241: c_unsorted,A__questionmark_lu0_242: c_unsorted] :
    ? [A__questionmark_v_0_116: c_type] :
      ( ( A__questionmark_v_0_116 = memory(A__questionmark_t1u0_238,A__questionmark_t2u0_237) )
      & ( not_assigns(c_sort(alloc_table(A__questionmark_t1u0_238),A__questionmark_au0_239),c_sort(A__questionmark_v_0_116,A__questionmark_m1u0_240),c_sort(A__questionmark_v_0_116,A__questionmark_m2u0_241),c_sort(pset(A__questionmark_t1u0_238),A__questionmark_lu0_242))
      <=> ! [A__questionmark_pu321_243: c_unsorted] :
          ? [A__questionmark_v_1_117: c_sorted] :
            ( ( A__questionmark_v_1_117 = c_sort(pointer(A__questionmark_t1u0_238),A__questionmark_pu321_243) )
            & ( ( valid(c_sort(alloc_table(A__questionmark_t1u0_238),A__questionmark_au0_239),A__questionmark_v_1_117)
                & ~ in_pset(A__questionmark_v_1_117,c_sort(pset(A__questionmark_t1u0_238),A__questionmark_lu0_242)) )
             => ( c_sort(A__questionmark_t2u0_237,smtlib__select(c_sort(A__questionmark_v_0_116,A__questionmark_m2u0_241),A__questionmark_v_1_117)) = c_sort(A__questionmark_t2u0_237,smtlib__select(c_sort(A__questionmark_v_0_116,A__questionmark_m1u0_240),A__questionmark_v_1_117)) ) ) ) ) ) ).

tff(formula_87,axiom,
    ! [A__questionmark_t2u0_244: c_type,A__questionmark_t1u0_245: c_type,A__questionmark_au324_246: c_unsorted,A__questionmark_mu323_247: c_unsorted,A__questionmark_lu322_248: c_unsorted] :
    ? [A__questionmark_v_0_118: c_sorted] :
      ( ( A__questionmark_v_0_118 = c_sort(memory(A__questionmark_t1u0_245,A__questionmark_t2u0_244),A__questionmark_mu323_247) )
      & not_assigns(c_sort(alloc_table(A__questionmark_t1u0_245),A__questionmark_au324_246),A__questionmark_v_0_118,A__questionmark_v_0_118,c_sort(pset(A__questionmark_t1u0_245),A__questionmark_lu322_248)) ) ).

tff(formula_88,axiom,
    ! [A__questionmark_t2u0_249: c_type,A__questionmark_t1u0_250: c_type,A__questionmark_au329_251: c_unsorted,A__questionmark_m1u328_252: c_unsorted,A__questionmark_m2u327_253: c_unsorted,A__questionmark_m3u326_254: c_unsorted,A__questionmark_lu325_255: c_unsorted] :
    ? [A__questionmark_v_1_119: c_sorted,A__questionmark_v_0_120: c_type] :
      ( ( A__questionmark_v_1_119 = c_sort(alloc_table(A__questionmark_t1u0_250),A__questionmark_au329_251) )
      & ( A__questionmark_v_0_120 = memory(A__questionmark_t1u0_250,A__questionmark_t2u0_249) )
      & ? [A__questionmark_v_4_121: c_sorted,A__questionmark_v_2_122: c_sorted,A__questionmark_v_3_123: c_sorted,A__questionmark_v_5_124: c_sorted] :
          ( ( A__questionmark_v_4_121 = c_sort(A__questionmark_v_0_120,A__questionmark_m1u328_252) )
          & ( A__questionmark_v_2_122 = c_sort(A__questionmark_v_0_120,A__questionmark_m2u327_253) )
          & ( A__questionmark_v_3_123 = c_sort(pset(A__questionmark_t1u0_250),A__questionmark_lu325_255) )
          & ( A__questionmark_v_5_124 = c_sort(A__questionmark_v_0_120,A__questionmark_m3u326_254) )
          & ( not_assigns(A__questionmark_v_1_119,A__questionmark_v_4_121,A__questionmark_v_2_122,A__questionmark_v_3_123)
           => ( not_assigns(A__questionmark_v_1_119,A__questionmark_v_2_122,A__questionmark_v_5_124,A__questionmark_v_3_123)
             => not_assigns(A__questionmark_v_1_119,A__questionmark_v_4_121,A__questionmark_v_5_124,A__questionmark_v_3_123) ) ) ) ) ).

tff(formula_89,axiom,
    ! [A__questionmark_t1u0_256: c_type,A__questionmark_pu332_257: c_unsorted,A__questionmark_qu331_258: c_unsorted,A__questionmark_iu330_259: $int] :
    ? [A__questionmark_v_0_125: c_type] :
      ( ( A__questionmark_v_0_125 = pointer(A__questionmark_t1u0_256) )
      & ? [A__questionmark_v_1_126: c_sorted,A__questionmark_v_2_127: c_sorted] :
          ( ( A__questionmark_v_1_126 = c_sort(A__questionmark_v_0_125,A__questionmark_pu332_257) )
          & ( A__questionmark_v_2_127 = c_sort(A__questionmark_v_0_125,A__questionmark_qu331_258) )
          & ( full_separated(A__questionmark_v_1_126,A__questionmark_v_2_127)
           => full_separated(A__questionmark_v_1_126,c_sort(A__questionmark_v_0_125,shift(A__questionmark_v_2_127,A__questionmark_iu330_259))) ) ) ) ).

tff(formula_90,axiom,
    ! [A__questionmark_t1u0_260: c_type,A__questionmark_pu335_261: c_unsorted,A__questionmark_qu334_262: c_unsorted,A__questionmark_iu333_263: $int] :
    ? [A__questionmark_v_0_128: c_type] :
      ( ( A__questionmark_v_0_128 = pointer(A__questionmark_t1u0_260) )
      & ? [A__questionmark_v_2_129: c_sorted,A__questionmark_v_1_130: c_sorted] :
          ( ( A__questionmark_v_2_129 = c_sort(A__questionmark_v_0_128,A__questionmark_pu335_261) )
          & ( A__questionmark_v_1_130 = c_sort(A__questionmark_v_0_128,A__questionmark_qu334_262) )
          & ( full_separated(A__questionmark_v_2_129,A__questionmark_v_1_130)
           => full_separated(c_sort(A__questionmark_v_0_128,shift(A__questionmark_v_1_130,A__questionmark_iu333_263)),A__questionmark_v_2_129) ) ) ) ).

tff(formula_91,axiom,
    ! [A__questionmark_t1u0_264: c_type,A__questionmark_pu338_265: c_unsorted,A__questionmark_qu337_266: c_unsorted,A__questionmark_iu336_267: $int] :
    ? [A__questionmark_v_0_131: c_type] :
      ( ( A__questionmark_v_0_131 = pointer(A__questionmark_t1u0_264) )
      & ? [A__questionmark_v_1_132: c_sorted,A__questionmark_v_2_133: c_sorted] :
          ( ( A__questionmark_v_1_132 = c_sort(A__questionmark_v_0_131,A__questionmark_qu337_266) )
          & ( A__questionmark_v_2_133 = c_sort(A__questionmark_v_0_131,A__questionmark_pu338_265) )
          & ( full_separated(A__questionmark_v_1_132,A__questionmark_v_2_133)
           => full_separated(c_sort(A__questionmark_v_0_131,shift(A__questionmark_v_1_132,A__questionmark_iu336_267)),A__questionmark_v_2_133) ) ) ) ).

tff(formula_92,axiom,
    ! [A__questionmark_t1u0_268: c_type,A__questionmark_pu341_269: c_unsorted,A__questionmark_qu340_270: c_unsorted,A__questionmark_iu339_271: $int] :
    ? [A__questionmark_v_0_134: c_type] :
      ( ( A__questionmark_v_0_134 = pointer(A__questionmark_t1u0_268) )
      & ? [A__questionmark_v_2_135: c_sorted,A__questionmark_v_1_136: c_sorted] :
          ( ( A__questionmark_v_2_135 = c_sort(A__questionmark_v_0_134,A__questionmark_qu340_270) )
          & ( A__questionmark_v_1_136 = c_sort(A__questionmark_v_0_134,A__questionmark_pu341_269) )
          & ( full_separated(A__questionmark_v_2_135,A__questionmark_v_1_136)
           => full_separated(A__questionmark_v_1_136,c_sort(A__questionmark_v_0_134,shift(A__questionmark_v_2_135,A__questionmark_iu339_271))) ) ) ) ).

tff(formula_93,axiom,
    ! [A__questionmark_t1u0_272: c_type,A__questionmark_t1u343_273: c_unsorted,A__questionmark_t2u342_274: c_unsorted] :
    ? [A__questionmark_v_0_137: c_type] :
      ( ( A__questionmark_v_0_137 = tag_id(A__questionmark_t1u0_272) )
      & ? [A__questionmark_v_1_138: c_sorted,A__questionmark_v_2_139: c_sorted] :
          ( ( A__questionmark_v_1_138 = c_sort(A__questionmark_v_0_137,A__questionmark_t1u343_273) )
          & ( A__questionmark_v_2_139 = c_sort(A__questionmark_v_0_137,A__questionmark_t2u342_274) )
          & ( ( subtag_bool(A__questionmark_v_1_138,A__questionmark_v_2_139) = c_Boolean_true )
          <=> subtag(A__questionmark_v_1_138,A__questionmark_v_2_139) ) ) ) ).

tff(formula_94,axiom,
    ! [A__questionmark_t1u0_275: c_type,A__questionmark_tu344_276: c_unsorted] :
    ? [A__questionmark_v_0_140: c_sorted] :
      ( ( A__questionmark_v_0_140 = c_sort(tag_id(A__questionmark_t1u0_275),A__questionmark_tu344_276) )
      & subtag(A__questionmark_v_0_140,A__questionmark_v_0_140) ) ).

tff(formula_95,axiom,
    ! [A__questionmark_t1u0_277: c_type,A__questionmark_t1u347_278: c_unsorted,A__questionmark_t2u346_279: c_unsorted,A__questionmark_t3u345_280: c_unsorted] :
    ? [A__questionmark_v_0_141: c_type] :
      ( ( A__questionmark_v_0_141 = tag_id(A__questionmark_t1u0_277) )
      & ? [A__questionmark_v_2_142: c_sorted,A__questionmark_v_1_143: c_sorted,A__questionmark_v_3_144: c_sorted] :
          ( ( A__questionmark_v_2_142 = c_sort(A__questionmark_v_0_141,A__questionmark_t1u347_278) )
          & ( A__questionmark_v_1_143 = c_sort(A__questionmark_v_0_141,A__questionmark_t2u346_279) )
          & ( A__questionmark_v_3_144 = c_sort(A__questionmark_v_0_141,A__questionmark_t3u345_280) )
          & ( subtag(A__questionmark_v_2_142,A__questionmark_v_1_143)
           => ( parenttag(A__questionmark_v_1_143,A__questionmark_v_3_144)
             => subtag(A__questionmark_v_2_142,A__questionmark_v_3_144) ) ) ) ) ).

tff(formula_96,axiom,
    ! [A__questionmark_t1u0_281: c_type,A__questionmark_au0_282: c_unsorted,A__questionmark_pu0_283: c_unsorted,A__questionmark_tu0_284: c_unsorted] :
    ? [A__questionmark_v_1_145: c_sorted,A__questionmark_v_2_146: c_sorted,A__questionmark_v_0_147: c_type] :
      ( ( A__questionmark_v_1_145 = c_sort(tag_table(A__questionmark_t1u0_281),A__questionmark_au0_282) )
      & ( A__questionmark_v_2_146 = c_sort(pointer(A__questionmark_t1u0_281),A__questionmark_pu0_283) )
      & ( A__questionmark_v_0_147 = tag_id(A__questionmark_t1u0_281) )
      & ? [A__questionmark_v_3_148: c_sorted] :
          ( ( A__questionmark_v_3_148 = c_sort(A__questionmark_v_0_147,A__questionmark_tu0_284) )
          & ( instanceof(A__questionmark_v_1_145,A__questionmark_v_2_146,A__questionmark_v_3_148)
          <=> subtag(c_sort(A__questionmark_v_0_147,typeof(A__questionmark_v_1_145,A__questionmark_v_2_146)),A__questionmark_v_3_148) ) ) ) ).

tff(formula_97,axiom,
    ! [A__questionmark_t1u0_285: c_type,A__questionmark_au353_286: c_unsorted,A__questionmark_pu352_287: c_unsorted,A__questionmark_su351_288: c_unsorted] :
    ? [A__questionmark_v_1_149: c_sorted,A__questionmark_v_0_150: c_type] :
      ( ( A__questionmark_v_1_149 = c_sort(tag_table(A__questionmark_t1u0_285),A__questionmark_au353_286) )
      & ( A__questionmark_v_0_150 = pointer(A__questionmark_t1u0_285) )
      & ? [A__questionmark_v_2_151: c_sorted,A__questionmark_v_3_152: c_sorted] :
          ( ( A__questionmark_v_2_151 = c_sort(A__questionmark_v_0_150,A__questionmark_pu352_287) )
          & ( A__questionmark_v_3_152 = c_sort(tag_id(A__questionmark_t1u0_285),A__questionmark_su351_288) )
          & ( instanceof(A__questionmark_v_1_149,A__questionmark_v_2_151,A__questionmark_v_3_152)
           => ( c_sort(A__questionmark_v_0_150,downcast(A__questionmark_v_1_149,A__questionmark_v_2_151,A__questionmark_v_3_152)) = A__questionmark_v_2_151 ) ) ) ) ).

tff(formula_98,axiom,
    ! [A__questionmark_t1u0_289: c_type,A__questionmark_tu360_290: c_unsorted] :
    ? [A__questionmark_v_0_153: c_type] :
      ( ( A__questionmark_v_0_153 = tag_id(A__questionmark_t1u0_289) )
      & subtag(c_sort(A__questionmark_v_0_153,A__questionmark_tu360_290),c_sort(A__questionmark_v_0_153,bottom_tag)) ) ).

tff(formula_99,axiom,
    ! [A__questionmark_t1u0_291: c_type,A__questionmark_tu0_292: c_unsorted] :
    ? [A__questionmark_v_1_154: c_type] :
      ( ( A__questionmark_v_1_154 = tag_id(A__questionmark_t1u0_291) )
      & ? [A__questionmark_v_0_155: c_sorted] :
          ( ( A__questionmark_v_0_155 = c_sort(A__questionmark_v_1_154,A__questionmark_tu0_292) )
          & ( root_tag(A__questionmark_v_0_155)
          <=> parenttag(A__questionmark_v_0_155,c_sort(A__questionmark_v_1_154,bottom_tag)) ) ) ) ).

tff(formula_100,axiom,
    ! [A__questionmark_t1u0_293: c_type,A__questionmark_au363_294: c_unsorted,A__questionmark_bu362_295: c_unsorted,A__questionmark_cu361_296: c_unsorted] :
    ? [A__questionmark_v_0_156: c_type] :
      ( ( A__questionmark_v_0_156 = tag_id(A__questionmark_t1u0_293) )
      & ? [A__questionmark_v_1_157: c_sorted,A__questionmark_v_2_158: c_sorted,A__questionmark_v_3_159: c_sorted] :
          ( ( A__questionmark_v_1_157 = c_sort(A__questionmark_v_0_156,A__questionmark_au363_294) )
          & ( A__questionmark_v_2_158 = c_sort(A__questionmark_v_0_156,A__questionmark_bu362_295) )
          & ( A__questionmark_v_3_159 = c_sort(A__questionmark_v_0_156,A__questionmark_cu361_296) )
          & ( root_tag(A__questionmark_v_1_157)
           => ( root_tag(A__questionmark_v_2_158)
             => ( ( A__questionmark_v_1_157 != A__questionmark_v_2_158 )
               => ( subtag(A__questionmark_v_3_159,A__questionmark_v_1_157)
                 => ~ subtag(A__questionmark_v_3_159,A__questionmark_v_2_158) ) ) ) ) ) ) ).

tff(formula_101,axiom,
    ! [A__questionmark_t1u0_297: c_type,A__questionmark_tagutableu0_298: c_unsorted,A__questionmark_mutableu0_299: c_unsorted,A__questionmark_thisu0_300: c_unsorted] :
    ? [A__questionmark_v_3_160: c_sorted,A__questionmark_v_0_161: c_type] :
      ( ( A__questionmark_v_3_160 = c_sort(tag_table(A__questionmark_t1u0_297),A__questionmark_tagutableu0_298) )
      & ( A__questionmark_v_0_161 = tag_id(A__questionmark_t1u0_297) )
      & ? [A__questionmark_v_1_162: c_sorted,A__questionmark_v_2_163: c_sorted] :
          ( ( A__questionmark_v_1_162 = c_sort(memory(A__questionmark_t1u0_297,A__questionmark_v_0_161),A__questionmark_mutableu0_299) )
          & ( A__questionmark_v_2_163 = c_sort(pointer(A__questionmark_t1u0_297),A__questionmark_thisu0_300) )
          & ( fully_packed(A__questionmark_v_3_160,A__questionmark_v_1_162,A__questionmark_v_2_163)
          <=> ( c_sort(A__questionmark_v_0_161,smtlib__select(A__questionmark_v_1_162,A__questionmark_v_2_163)) = c_sort(A__questionmark_v_0_161,typeof(A__questionmark_v_3_160,A__questionmark_v_2_163)) ) ) ) ) ).

tff(formula_102,axiom,
    ! [A__questionmark_au369_301: $int,A__questionmark_bu368_302: $int] :
      ( ( bw_and(A__questionmark_au369_301,A__questionmark_bu368_302) != 0 )
     => ( ( A__questionmark_au369_301 != 0 )
        & ( A__questionmark_bu368_302 != 0 ) ) ) ).

tff(formula_103,axiom,
    ! [A__questionmark_au371_303: $int,A__questionmark_bu370_304: $int] :
      ( ( $lesseq(0,A__questionmark_au371_303)
        & $lesseq(0,A__questionmark_bu370_304) )
     => $lesseq(0,lsl(A__questionmark_au371_303,A__questionmark_bu370_304)) ) ).

tff(formula_104,axiom,
    ! [A__questionmark_a1u374_305: $int,A__questionmark_a2u373_306: $int,A__questionmark_bu372_307: $int] :
      ( ( $lesseq(0,A__questionmark_a1u374_305)
        & $lesseq(A__questionmark_a1u374_305,A__questionmark_a2u373_306)
        & $lesseq(0,A__questionmark_bu372_307) )
     => $lesseq(lsl(A__questionmark_a1u374_305,A__questionmark_bu372_307),lsl(A__questionmark_a2u373_306,A__questionmark_bu372_307)) ) ).

tff(formula_105,axiom,
    ! [A__questionmark_au376_308: $int,A__questionmark_bu375_309: $int] :
      ( ( $lesseq(0,A__questionmark_au376_308)
        & $lesseq(0,A__questionmark_bu375_309) )
     => $lesseq(0,lsr(A__questionmark_au376_308,A__questionmark_bu375_309)) ) ).

tff(formula_106,axiom,
    ! [A__questionmark_au378_310: $int,A__questionmark_bu377_311: $int] :
      ( ( $lesseq(0,A__questionmark_au378_310)
        & $lesseq(0,A__questionmark_bu377_311) )
     => $lesseq(lsr(A__questionmark_au378_310,A__questionmark_bu377_311),A__questionmark_au378_310) ) ).

tff(formula_107,axiom,
    ! [A__questionmark_au380_312: $int,A__questionmark_bu379_313: $int] :
      ( ( $lesseq(0,A__questionmark_au380_312)
        & $lesseq(0,A__questionmark_bu379_313) )
     => $lesseq(0,asr(A__questionmark_au380_312,A__questionmark_bu379_313)) ) ).

tff(formula_108,axiom,
    ! [A__questionmark_au382_314: $int,A__questionmark_bu381_315: $int] :
      ( ( $lesseq(0,A__questionmark_au382_314)
        & $lesseq(0,A__questionmark_bu381_315) )
     => $lesseq(asr(A__questionmark_au382_314,A__questionmark_bu381_315),A__questionmark_au382_314) ) ).

tff(formula_109,axiom,
    ! [A__questionmark_au384_316: $int,A__questionmark_bu383_317: $int] :
      ( ( $lesseq(0,A__questionmark_au384_316)
        & $lesseq(0,A__questionmark_bu383_317) )
     => ( asr(A__questionmark_au384_316,A__questionmark_bu383_317) = lsr(A__questionmark_au384_316,A__questionmark_bu383_317) ) ) ).

tff(formula_110,axiom,
    ! [A__questionmark_au386_318: $int,A__questionmark_bu385_319: $int] :
      ( ( $lesseq(0,A__questionmark_au386_318)
        & $lesseq(0,A__questionmark_bu385_319) )
     => $lesseq(lsl(lsr(A__questionmark_au386_318,A__questionmark_bu385_319),A__questionmark_bu385_319),A__questionmark_au386_318) ) ).

tff(formula_111,axiom,
    ! [A__questionmark_au388_320: $int,A__questionmark_bu387_321: $int] :
      ( ( $lesseq(0,A__questionmark_au388_320)
        & $lesseq(0,A__questionmark_bu387_321) )
     => ( lsr(lsl(A__questionmark_au388_320,A__questionmark_bu387_321),A__questionmark_bu387_321) = A__questionmark_au388_320 ) ) ).

tff(formula_112,axiom,
    ! [A__questionmark_t1u0_322: c_type,A__questionmark_au0_323: c_unsorted,A__questionmark_pu0_324: c_unsorted,A__questionmark_nu0_325: $int] :
      ( alloc_fresh(c_sort(alloc_table(A__questionmark_t1u0_322),A__questionmark_au0_323),c_sort(pointer(A__questionmark_t1u0_322),A__questionmark_pu0_324),A__questionmark_nu0_325)
    <=> ! [A__questionmark_iu389_326: $int] :
        ? [A__questionmark_v_0_164: c_type] :
          ( ( A__questionmark_v_0_164 = pointer(A__questionmark_t1u0_322) )
          & ( ( $lesseq(0,A__questionmark_iu389_326)
              & $less(A__questionmark_iu389_326,A__questionmark_nu0_325) )
           => ~ valid(c_sort(alloc_table(A__questionmark_t1u0_322),A__questionmark_au0_323),c_sort(A__questionmark_v_0_164,shift(c_sort(A__questionmark_v_0_164,A__questionmark_pu0_324),A__questionmark_iu389_326))) ) ) ) ).

tff(formula_113,axiom,
    ! [A__questionmark_t1u0_327: c_type,A__questionmark_a1u392_328: c_unsorted,A__questionmark_a2u391_329: c_unsorted] :
    ? [A__questionmark_v_0_165: c_type] :
      ( ( A__questionmark_v_0_165 = alloc_table(A__questionmark_t1u0_327) )
      & ( alloc_extends(c_sort(A__questionmark_v_0_165,A__questionmark_a1u392_328),c_sort(A__questionmark_v_0_165,A__questionmark_a2u391_329))
       => ! [A__questionmark_pu390_330: c_unsorted] :
          ? [A__questionmark_v_1_166: c_sorted,A__questionmark_v_2_167: c_sorted] :
            ( ( A__questionmark_v_1_166 = c_sort(A__questionmark_v_0_165,A__questionmark_a1u392_328) )
            & ( A__questionmark_v_2_167 = c_sort(pointer(A__questionmark_t1u0_327),A__questionmark_pu390_330) )
            & ( valid(A__questionmark_v_1_166,A__questionmark_v_2_167)
             => ( offset_min(A__questionmark_v_1_166,A__questionmark_v_2_167) = offset_min(c_sort(A__questionmark_v_0_165,A__questionmark_a2u391_329),A__questionmark_v_2_167) ) ) ) ) ) ).

tff(formula_114,axiom,
    ! [A__questionmark_t1u0_331: c_type,A__questionmark_a1u395_332: c_unsorted,A__questionmark_a2u394_333: c_unsorted] :
    ? [A__questionmark_v_0_168: c_type] :
      ( ( A__questionmark_v_0_168 = alloc_table(A__questionmark_t1u0_331) )
      & ( alloc_extends(c_sort(A__questionmark_v_0_168,A__questionmark_a1u395_332),c_sort(A__questionmark_v_0_168,A__questionmark_a2u394_333))
       => ! [A__questionmark_pu393_334: c_unsorted] :
          ? [A__questionmark_v_1_169: c_sorted,A__questionmark_v_2_170: c_sorted] :
            ( ( A__questionmark_v_1_169 = c_sort(A__questionmark_v_0_168,A__questionmark_a1u395_332) )
            & ( A__questionmark_v_2_170 = c_sort(pointer(A__questionmark_t1u0_331),A__questionmark_pu393_334) )
            & ( valid(A__questionmark_v_1_169,A__questionmark_v_2_170)
             => ( offset_max(A__questionmark_v_1_169,A__questionmark_v_2_170) = offset_max(c_sort(A__questionmark_v_0_168,A__questionmark_a2u394_333),A__questionmark_v_2_170) ) ) ) ) ) ).

tff(formula_115,axiom,
    ! [A__questionmark_t2u0_335: c_type,A__questionmark_t1u0_336: c_type,A__questionmark_a1u402_337: c_unsorted,A__questionmark_a2u401_338: c_unsorted,A__questionmark_m1u400_339: c_unsorted,A__questionmark_m2u399_340: c_unsorted,A__questionmark_lu398_341: c_unsorted,A__questionmark_pu397_342: c_unsorted,A__questionmark_nu396_343: $int] :
    ? [A__questionmark_v_0_171: c_type] :
      ( ( A__questionmark_v_0_171 = alloc_table(A__questionmark_t1u0_336) )
      & ? [A__questionmark_v_1_172: c_sorted,A__questionmark_v_2_173: c_sorted,A__questionmark_v_6_174: c_sorted,A__questionmark_v_3_175: c_type] :
          ( ( A__questionmark_v_1_172 = c_sort(A__questionmark_v_0_171,A__questionmark_a1u402_337) )
          & ( A__questionmark_v_2_173 = c_sort(A__questionmark_v_0_171,A__questionmark_a2u401_338) )
          & ( A__questionmark_v_6_174 = c_sort(pointer(A__questionmark_t1u0_336),A__questionmark_pu397_342) )
          & ( A__questionmark_v_3_175 = memory(A__questionmark_t1u0_336,A__questionmark_t2u0_335) )
          & ? [A__questionmark_v_7_176: c_sorted,A__questionmark_v_8_177: c_sorted,A__questionmark_v_5_178: c_type] :
              ( ( A__questionmark_v_7_176 = c_sort(A__questionmark_v_3_175,A__questionmark_m1u400_339) )
              & ( A__questionmark_v_8_177 = c_sort(A__questionmark_v_3_175,A__questionmark_m2u399_340) )
              & ( A__questionmark_v_5_178 = pset(A__questionmark_t1u0_336) )
              & ? [A__questionmark_v_4_179: c_sorted] :
                  ( ( A__questionmark_v_4_179 = c_sort(A__questionmark_v_5_178,A__questionmark_lu398_341) )
                  & ( ( alloc_extends(A__questionmark_v_1_172,A__questionmark_v_2_173)
                      & alloc_fresh(A__questionmark_v_1_172,A__questionmark_v_6_174,A__questionmark_nu396_343)
                      & not_assigns(A__questionmark_v_2_173,A__questionmark_v_7_176,A__questionmark_v_8_177,A__questionmark_v_4_179)
                      & pset_included(A__questionmark_v_4_179,c_sort(A__questionmark_v_5_178,pset_all(c_sort(A__questionmark_v_5_178,pset_singleton(A__questionmark_v_6_174))))) )
                   => not_assigns(A__questionmark_v_1_172,A__questionmark_v_7_176,A__questionmark_v_8_177,c_sort(A__questionmark_v_5_178,pset_empty)) ) ) ) ) ) ).

tff(formula_116,axiom,
    ! [A__questionmark_t1u0_344: c_type,A__questionmark_a1u406_345: c_unsorted,A__questionmark_a2u405_346: c_unsorted,A__questionmark_lu404_347: c_unsorted] :
    ? [A__questionmark_v_0_180: c_type] :
      ( ( A__questionmark_v_0_180 = alloc_table(A__questionmark_t1u0_344) )
      & ( alloc_extends_except(c_sort(A__questionmark_v_0_180,A__questionmark_a1u406_345),c_sort(A__questionmark_v_0_180,A__questionmark_a2u405_346),c_sort(pset(A__questionmark_t1u0_344),A__questionmark_lu404_347))
       => ! [A__questionmark_pu403_348: c_unsorted] :
          ? [A__questionmark_v_2_181: c_sorted,A__questionmark_v_1_182: c_sorted] :
            ( ( A__questionmark_v_2_181 = c_sort(A__questionmark_v_0_180,A__questionmark_a1u406_345) )
            & ( A__questionmark_v_1_182 = c_sort(pointer(A__questionmark_t1u0_344),A__questionmark_pu403_348) )
            & ( ( valid(A__questionmark_v_2_181,A__questionmark_v_1_182)
                & ~ in_pset(A__questionmark_v_1_182,c_sort(pset(A__questionmark_t1u0_344),A__questionmark_lu404_347)) )
             => ( offset_min(A__questionmark_v_2_181,A__questionmark_v_1_182) = offset_min(c_sort(A__questionmark_v_0_180,A__questionmark_a2u405_346),A__questionmark_v_1_182) ) ) ) ) ) ).

tff(formula_117,axiom,
    ! [A__questionmark_t1u0_349: c_type,A__questionmark_a1u410_350: c_unsorted,A__questionmark_a2u409_351: c_unsorted,A__questionmark_lu408_352: c_unsorted] :
    ? [A__questionmark_v_0_183: c_type] :
      ( ( A__questionmark_v_0_183 = alloc_table(A__questionmark_t1u0_349) )
      & ( alloc_extends_except(c_sort(A__questionmark_v_0_183,A__questionmark_a1u410_350),c_sort(A__questionmark_v_0_183,A__questionmark_a2u409_351),c_sort(pset(A__questionmark_t1u0_349),A__questionmark_lu408_352))
       => ! [A__questionmark_pu407_353: c_unsorted] :
          ? [A__questionmark_v_2_184: c_sorted,A__questionmark_v_1_185: c_sorted] :
            ( ( A__questionmark_v_2_184 = c_sort(A__questionmark_v_0_183,A__questionmark_a1u410_350) )
            & ( A__questionmark_v_1_185 = c_sort(pointer(A__questionmark_t1u0_349),A__questionmark_pu407_353) )
            & ( ( valid(A__questionmark_v_2_184,A__questionmark_v_1_185)
                & ~ in_pset(A__questionmark_v_1_185,c_sort(pset(A__questionmark_t1u0_349),A__questionmark_lu408_352)) )
             => ( offset_max(A__questionmark_v_2_184,A__questionmark_v_1_185) = offset_max(c_sort(A__questionmark_v_0_183,A__questionmark_a2u409_351),A__questionmark_v_1_185) ) ) ) ) ) ).

tff(formula_118,axiom,
    ! [A__questionmark_t1u0_354: c_type,A__questionmark_au434_355: c_unsorted,A__questionmark_pu433_356: c_unsorted,A__questionmark_su432_357: $int] :
    ? [A__questionmark_v_0_186: c_sorted,A__questionmark_v_1_187: c_sorted] :
      ( ( A__questionmark_v_0_186 = c_sort(alloc_table(A__questionmark_t1u0_354),A__questionmark_au434_355) )
      & ( A__questionmark_v_1_187 = c_sort(pointer(A__questionmark_t1u0_354),A__questionmark_pu433_356) )
      & ? [A__questionmark_v_2_188: $int,A__questionmark_v_3_189: $int] :
          ( ( A__questionmark_v_2_188 = $product(A__questionmark_su432_357,offset_min_bytes(A__questionmark_v_0_186,A__questionmark_v_1_187,A__questionmark_su432_357)) )
          & ( A__questionmark_v_3_189 = offset_min(A__questionmark_v_0_186,A__questionmark_v_1_187) )
          & ( $less(0,A__questionmark_su432_357)
           => ( $lesseq(A__questionmark_v_3_189,A__questionmark_v_2_188)
              & $less($difference(A__questionmark_v_2_188,A__questionmark_su432_357),A__questionmark_v_3_189) ) ) ) ) ).

tff(formula_119,axiom,
    ! [A__questionmark_t1u0_358: c_type,A__questionmark_au437_359: c_unsorted,A__questionmark_pu436_360: c_unsorted,A__questionmark_su435_361: $int] :
    ? [A__questionmark_v_0_190: c_sorted,A__questionmark_v_1_191: c_sorted] :
      ( ( A__questionmark_v_0_190 = c_sort(alloc_table(A__questionmark_t1u0_358),A__questionmark_au437_359) )
      & ( A__questionmark_v_1_191 = c_sort(pointer(A__questionmark_t1u0_358),A__questionmark_pu436_360) )
      & ? [A__questionmark_v_2_192: $int,A__questionmark_v_3_193: $int] :
          ( ( A__questionmark_v_2_192 = offset_max(A__questionmark_v_0_190,A__questionmark_v_1_191) )
          & ( A__questionmark_v_3_193 = $sum($product(A__questionmark_su435_361,offset_max_bytes(A__questionmark_v_0_190,A__questionmark_v_1_191,A__questionmark_su435_361)),A__questionmark_su435_361) )
          & ( $less(0,A__questionmark_su435_361)
           => ( $lesseq($difference(A__questionmark_v_3_193,1),A__questionmark_v_2_192)
              & $less(A__questionmark_v_2_192,$difference($sum(A__questionmark_v_3_193,A__questionmark_su435_361),1)) ) ) ) ) ).

tff(formula_120,axiom,
    ! [A__questionmark_o1u443_362: $int,A__questionmark_s1u442_363: $int,A__questionmark_o2u441_364: $int,A__questionmark_s2u440_365: $int,A__questionmark_v1u439_366: c_unsorted,A__questionmark_v2u438_367: c_unsorted] :
    ? [A__questionmark_v_0_194: c_sorted] :
      ( ( A__questionmark_v_0_194 = c_sort(bitvector,A__questionmark_v2u438_367) )
      & ( ( ( A__questionmark_o1u443_362 = A__questionmark_o2u441_364 )
          & ( A__questionmark_s1u442_363 = A__questionmark_s2u440_365 ) )
       => ( c_sort(bitvector,extract_bytes(c_sort(bitvector,replace_bytes(c_sort(bitvector,A__questionmark_v1u439_366),A__questionmark_o1u443_362,A__questionmark_s1u442_363,A__questionmark_v_0_194)),A__questionmark_o2u441_364,A__questionmark_s2u440_365)) = A__questionmark_v_0_194 ) ) ) ).

tff(formula_121,axiom,
    ! [A__questionmark_o1u449_368: $int,A__questionmark_s1u448_369: $int,A__questionmark_o2u447_370: $int,A__questionmark_s2u446_371: $int,A__questionmark_v1u445_372: c_unsorted,A__questionmark_v2u444_373: c_unsorted] :
    ? [A__questionmark_v_0_195: c_sorted] :
      ( ( A__questionmark_v_0_195 = c_sort(bitvector,A__questionmark_v1u445_372) )
      & ( ( $lesseq($sum(A__questionmark_o2u447_370,A__questionmark_s2u446_371),A__questionmark_o1u449_368)
          | $lesseq($sum(A__questionmark_o1u449_368,A__questionmark_s2u446_371),A__questionmark_o2u447_370) )
       => ( c_sort(bitvector,extract_bytes(c_sort(bitvector,replace_bytes(A__questionmark_v_0_195,A__questionmark_o1u449_368,A__questionmark_s1u448_369,c_sort(bitvector,A__questionmark_v2u444_373))),A__questionmark_o2u447_370,A__questionmark_s2u446_371)) = c_sort(bitvector,extract_bytes(A__questionmark_v_0_195,A__questionmark_o2u447_370,A__questionmark_s2u446_371)) ) ) ) ).

tff(formula_122,axiom,
    ! [A__questionmark_o1u456_374: $int,A__questionmark_s1u455_375: $int,A__questionmark_o2u454_376: $int,A__questionmark_s2u453_377: $int,A__questionmark_v1u452_378: c_unsorted,A__questionmark_v2u451_379: c_unsorted,A__questionmark_v3u450_380: c_unsorted] :
    ? [A__questionmark_v_0_196: c_sorted,A__questionmark_v_1_197: c_sorted,A__questionmark_v_2_198: c_sorted] :
      ( ( A__questionmark_v_0_196 = c_sort(bitvector,A__questionmark_v1u452_378) )
      & ( A__questionmark_v_1_197 = c_sort(bitvector,A__questionmark_v2u451_379) )
      & ( A__questionmark_v_2_198 = c_sort(bitvector,A__questionmark_v3u450_380) )
      & ( ( $sum(A__questionmark_o1u456_374,A__questionmark_s1u455_375) = A__questionmark_o2u454_376 )
       => ( c_sort(bitvector,replace_bytes(c_sort(bitvector,replace_bytes(A__questionmark_v_0_196,A__questionmark_o1u456_374,A__questionmark_s1u455_375,A__questionmark_v_1_197)),A__questionmark_o2u454_376,A__questionmark_s2u453_377,A__questionmark_v_2_198)) = c_sort(bitvector,replace_bytes(A__questionmark_v_0_196,A__questionmark_o1u456_374,$sum(A__questionmark_s1u455_375,A__questionmark_s2u453_377),c_sort(bitvector,concat_bitvector(A__questionmark_v_1_197,A__questionmark_v_2_198)))) ) ) ) ).

tff(formula_123,axiom,
    ! [A__questionmark_o1u463_381: $int,A__questionmark_s1u462_382: $int,A__questionmark_o2u461_383: $int,A__questionmark_s2u460_384: $int,A__questionmark_v1u459_385: c_unsorted,A__questionmark_v2u458_386: c_unsorted,A__questionmark_v3u457_387: c_unsorted] :
    ? [A__questionmark_v_0_199: c_sorted,A__questionmark_v_2_200: c_sorted,A__questionmark_v_1_201: c_sorted] :
      ( ( A__questionmark_v_0_199 = c_sort(bitvector,A__questionmark_v1u459_385) )
      & ( A__questionmark_v_2_200 = c_sort(bitvector,A__questionmark_v2u458_386) )
      & ( A__questionmark_v_1_201 = c_sort(bitvector,A__questionmark_v3u457_387) )
      & ( ( $sum(A__questionmark_o2u461_383,A__questionmark_s2u460_384) = A__questionmark_o1u463_381 )
       => ( c_sort(bitvector,replace_bytes(c_sort(bitvector,replace_bytes(A__questionmark_v_0_199,A__questionmark_o1u463_381,A__questionmark_s1u462_382,A__questionmark_v_2_200)),A__questionmark_o2u461_383,A__questionmark_s2u460_384,A__questionmark_v_1_201)) = c_sort(bitvector,replace_bytes(A__questionmark_v_0_199,A__questionmark_o2u461_383,$sum(A__questionmark_s1u462_382,A__questionmark_s2u460_384),c_sort(bitvector,concat_bitvector(A__questionmark_v_1_201,A__questionmark_v_2_200)))) ) ) ) ).

tff(formula_124,axiom,
    ! [A__questionmark_o1u468_388: $int,A__questionmark_s1u467_389: $int,A__questionmark_o2u466_390: $int,A__questionmark_s2u465_391: $int,A__questionmark_vu464_392: c_unsorted] :
    ? [A__questionmark_v_0_202: c_sorted] :
      ( ( A__questionmark_v_0_202 = c_sort(bitvector,A__questionmark_vu464_392) )
      & ( ( $sum(A__questionmark_o1u468_388,A__questionmark_s1u467_389) = A__questionmark_o2u466_390 )
       => ( c_sort(bitvector,concat_bitvector(c_sort(bitvector,extract_bytes(A__questionmark_v_0_202,A__questionmark_o1u468_388,A__questionmark_s1u467_389)),c_sort(bitvector,extract_bytes(A__questionmark_v_0_202,A__questionmark_o2u466_390,A__questionmark_s2u465_391)))) = c_sort(bitvector,extract_bytes(A__questionmark_v_0_202,A__questionmark_o1u468_388,$sum(A__questionmark_s1u467_389,A__questionmark_s2u465_391))) ) ) ) ).

tff(formula_125,axiom,
    ! [A__questionmark_t1u0_393: c_type,A__questionmark_mu476_394: c_unsorted,A__questionmark_p1u475_395: c_unsorted,A__questionmark_p2u474_396: c_unsorted,A__questionmark_o1u473_397: $int,A__questionmark_s1u472_398: $int,A__questionmark_o2u471_399: $int,A__questionmark_s2u470_400: $int,A__questionmark_vu469_401: c_unsorted] :
    ? [A__questionmark_v_0_203: c_type] :
      ( ( A__questionmark_v_0_203 = pointer(A__questionmark_t1u0_393) )
      & ? [A__questionmark_v_2_204: c_sorted,A__questionmark_v_3_205: c_sorted,A__questionmark_v_1_206: c_type,A__questionmark_v_4_207: c_sorted] :
          ( ( A__questionmark_v_2_204 = c_sort(A__questionmark_v_0_203,A__questionmark_p1u475_395) )
          & ( A__questionmark_v_3_205 = c_sort(A__questionmark_v_0_203,A__questionmark_p2u474_396) )
          & ( A__questionmark_v_1_206 = memory(A__questionmark_t1u0_393,bitvector) )
          & ( A__questionmark_v_4_207 = c_sort(bitvector,A__questionmark_vu469_401) )
          & ( ( ( A__questionmark_v_2_204 = A__questionmark_v_3_205 )
              & ( A__questionmark_o1u473_397 = A__questionmark_o2u471_399 )
              & ( A__questionmark_s1u472_398 = A__questionmark_s2u470_400 ) )
           => ( c_sort(bitvector,select_bytes(c_sort(A__questionmark_v_1_206,store_bytes(c_sort(A__questionmark_v_1_206,A__questionmark_mu476_394),A__questionmark_v_2_204,A__questionmark_o1u473_397,A__questionmark_s1u472_398,A__questionmark_v_4_207)),A__questionmark_v_3_205,A__questionmark_o2u471_399,A__questionmark_s2u470_400)) = A__questionmark_v_4_207 ) ) ) ) ).

tff(formula_126,axiom,
    ! [A__questionmark_t1u0_402: c_type,A__questionmark_mu484_403: c_unsorted,A__questionmark_p1u483_404: c_unsorted,A__questionmark_p2u482_405: c_unsorted,A__questionmark_o1u481_406: $int,A__questionmark_s1u480_407: $int,A__questionmark_o2u479_408: $int,A__questionmark_s2u478_409: $int,A__questionmark_vu477_410: c_unsorted] :
    ? [A__questionmark_v_0_208: c_type,A__questionmark_v_1_209: c_type] :
      ( ( A__questionmark_v_0_208 = pset(A__questionmark_t1u0_402) )
      & ( A__questionmark_v_1_209 = pointer(A__questionmark_t1u0_402) )
      & ? [A__questionmark_v_3_210: c_sorted,A__questionmark_v_4_211: c_sorted,A__questionmark_v_2_212: c_type] :
          ( ( A__questionmark_v_3_210 = c_sort(A__questionmark_v_1_209,A__questionmark_p1u483_404) )
          & ( A__questionmark_v_4_211 = c_sort(A__questionmark_v_1_209,A__questionmark_p2u482_405) )
          & ( A__questionmark_v_2_212 = memory(A__questionmark_t1u0_402,bitvector) )
          & ? [A__questionmark_v_5_213: c_sorted] :
              ( ( A__questionmark_v_5_213 = c_sort(A__questionmark_v_2_212,A__questionmark_mu484_403) )
              & ( pset_disjoint(c_sort(A__questionmark_v_0_208,pset_range(c_sort(A__questionmark_v_0_208,pset_singleton(A__questionmark_v_3_210)),A__questionmark_o1u481_406,$sum(A__questionmark_o1u481_406,A__questionmark_s1u480_407))),c_sort(A__questionmark_v_0_208,pset_range(c_sort(A__questionmark_v_0_208,pset_singleton(A__questionmark_v_4_211)),A__questionmark_o2u479_408,$sum(A__questionmark_o2u479_408,A__questionmark_s2u478_409))))
               => ( c_sort(bitvector,select_bytes(c_sort(A__questionmark_v_2_212,store_bytes(A__questionmark_v_5_213,A__questionmark_v_3_210,A__questionmark_o1u481_406,A__questionmark_s1u480_407,c_sort(bitvector,A__questionmark_vu477_410))),A__questionmark_v_4_211,A__questionmark_o2u479_408,A__questionmark_s2u478_409)) = c_sort(bitvector,select_bytes(A__questionmark_v_5_213,A__questionmark_v_4_211,A__questionmark_o2u479_408,A__questionmark_s2u478_409)) ) ) ) ) ) ).

tff(formula_127,axiom,
    ! [A__questionmark_t1u0_411: c_type,A__questionmark_mu490_412: c_unsorted,A__questionmark_pu489_413: c_unsorted,A__questionmark_iu488_414: $int,A__questionmark_ou487_415: $int,A__questionmark_su486_416: $int,A__questionmark_vu485_417: c_unsorted] :
    ? [A__questionmark_v_0_214: c_type] :
      ( ( A__questionmark_v_0_214 = memory(A__questionmark_t1u0_411,bitvector) )
      & ? [A__questionmark_v_2_215: c_sorted,A__questionmark_v_1_216: c_type] :
          ( ( A__questionmark_v_2_215 = c_sort(A__questionmark_v_0_214,A__questionmark_mu490_412) )
          & ( A__questionmark_v_1_216 = pointer(A__questionmark_t1u0_411) )
          & ? [A__questionmark_v_3_217: c_sorted,A__questionmark_v_4_218: c_sorted] :
              ( ( A__questionmark_v_3_217 = c_sort(A__questionmark_v_1_216,A__questionmark_pu489_413) )
              & ( A__questionmark_v_4_218 = c_sort(bitvector,A__questionmark_vu485_417) )
              & ( c_sort(A__questionmark_v_0_214,store_bytes(A__questionmark_v_2_215,c_sort(A__questionmark_v_1_216,shift(A__questionmark_v_3_217,A__questionmark_iu488_414)),A__questionmark_ou487_415,A__questionmark_su486_416,A__questionmark_v_4_218)) = c_sort(A__questionmark_v_0_214,store_bytes(A__questionmark_v_2_215,A__questionmark_v_3_217,$sum(A__questionmark_ou487_415,A__questionmark_iu488_414),A__questionmark_su486_416,A__questionmark_v_4_218)) ) ) ) ) ).

tff(formula_128,axiom,
    ! [A__questionmark_t1u0_418: c_type,A__questionmark_mu496_419: c_unsorted,A__questionmark_pu495_420: c_unsorted,A__questionmark_iu494_421: $int,A__questionmark_ou493_422: $int,A__questionmark_su492_423: $int,A__questionmark_vu491_424: c_unsorted] :
    ? [A__questionmark_v_1_219: c_sorted,A__questionmark_v_0_220: c_type] :
      ( ( A__questionmark_v_1_219 = c_sort(memory(A__questionmark_t1u0_418,bitvector),A__questionmark_mu496_419) )
      & ( A__questionmark_v_0_220 = pointer(A__questionmark_t1u0_418) )
      & ? [A__questionmark_v_2_221: c_sorted] :
          ( ( A__questionmark_v_2_221 = c_sort(A__questionmark_v_0_220,A__questionmark_pu495_420) )
          & ( c_sort(bitvector,select_bytes(A__questionmark_v_1_219,c_sort(A__questionmark_v_0_220,shift(A__questionmark_v_2_221,A__questionmark_iu494_421)),A__questionmark_ou493_422,A__questionmark_su492_423)) = c_sort(bitvector,select_bytes(A__questionmark_v_1_219,A__questionmark_v_2_221,$sum(A__questionmark_ou493_422,A__questionmark_iu494_421),A__questionmark_su492_423)) ) ) ) ).

tff(formula_129,axiom,
    ! [A__questionmark_t1u0_425: c_type,A__questionmark_mu504_426: c_unsorted,A__questionmark_pu503_427: c_unsorted,A__questionmark_o1u502_428: $int,A__questionmark_s1u501_429: $int,A__questionmark_o2u500_430: $int,A__questionmark_s2u499_431: $int,A__questionmark_v1u498_432: c_unsorted,A__questionmark_v2u497_433: c_unsorted] :
    ? [A__questionmark_v_0_222: c_type] :
      ( ( A__questionmark_v_0_222 = memory(A__questionmark_t1u0_425,bitvector) )
      & ? [A__questionmark_v_2_223: c_sorted,A__questionmark_v_1_224: c_sorted,A__questionmark_v_3_225: c_sorted,A__questionmark_v_4_226: c_sorted] :
          ( ( A__questionmark_v_2_223 = c_sort(A__questionmark_v_0_222,A__questionmark_mu504_426) )
          & ( A__questionmark_v_1_224 = c_sort(pointer(A__questionmark_t1u0_425),A__questionmark_pu503_427) )
          & ( A__questionmark_v_3_225 = c_sort(bitvector,A__questionmark_v1u498_432) )
          & ( A__questionmark_v_4_226 = c_sort(bitvector,A__questionmark_v2u497_433) )
          & ( ( $sum(A__questionmark_o1u502_428,A__questionmark_s1u501_429) = A__questionmark_o2u500_430 )
           => ( c_sort(A__questionmark_v_0_222,store_bytes(c_sort(A__questionmark_v_0_222,store_bytes(A__questionmark_v_2_223,A__questionmark_v_1_224,A__questionmark_o1u502_428,A__questionmark_s1u501_429,A__questionmark_v_3_225)),A__questionmark_v_1_224,A__questionmark_o2u500_430,A__questionmark_s2u499_431,A__questionmark_v_4_226)) = c_sort(A__questionmark_v_0_222,store_bytes(A__questionmark_v_2_223,A__questionmark_v_1_224,A__questionmark_o1u502_428,$sum(A__questionmark_s1u501_429,A__questionmark_s2u499_431),c_sort(bitvector,concat_bitvector(A__questionmark_v_3_225,A__questionmark_v_4_226)))) ) ) ) ) ).

tff(formula_130,axiom,
    ! [A__questionmark_t1u0_434: c_type,A__questionmark_mu512_435: c_unsorted,A__questionmark_pu511_436: c_unsorted,A__questionmark_o1u510_437: $int,A__questionmark_s1u509_438: $int,A__questionmark_o2u508_439: $int,A__questionmark_s2u507_440: $int,A__questionmark_v1u506_441: c_unsorted,A__questionmark_v2u505_442: c_unsorted] :
    ? [A__questionmark_v_0_227: c_type] :
      ( ( A__questionmark_v_0_227 = memory(A__questionmark_t1u0_434,bitvector) )
      & ? [A__questionmark_v_2_228: c_sorted,A__questionmark_v_1_229: c_sorted,A__questionmark_v_4_230: c_sorted,A__questionmark_v_3_231: c_sorted] :
          ( ( A__questionmark_v_2_228 = c_sort(A__questionmark_v_0_227,A__questionmark_mu512_435) )
          & ( A__questionmark_v_1_229 = c_sort(pointer(A__questionmark_t1u0_434),A__questionmark_pu511_436) )
          & ( A__questionmark_v_4_230 = c_sort(bitvector,A__questionmark_v1u506_441) )
          & ( A__questionmark_v_3_231 = c_sort(bitvector,A__questionmark_v2u505_442) )
          & ( ( $sum(A__questionmark_o2u508_439,A__questionmark_s2u507_440) = A__questionmark_o1u510_437 )
           => ( c_sort(A__questionmark_v_0_227,store_bytes(c_sort(A__questionmark_v_0_227,store_bytes(A__questionmark_v_2_228,A__questionmark_v_1_229,A__questionmark_o1u510_437,A__questionmark_s1u509_438,A__questionmark_v_4_230)),A__questionmark_v_1_229,A__questionmark_o2u508_439,A__questionmark_s2u507_440,A__questionmark_v_3_231)) = c_sort(A__questionmark_v_0_227,store_bytes(A__questionmark_v_2_228,A__questionmark_v_1_229,A__questionmark_o2u508_439,$sum(A__questionmark_s1u509_438,A__questionmark_s2u507_440),c_sort(bitvector,concat_bitvector(A__questionmark_v_3_231,A__questionmark_v_4_230)))) ) ) ) ) ).

tff(formula_131,axiom,
    ! [A__questionmark_t1u0_443: c_type,A__questionmark_mu518_444: c_unsorted,A__questionmark_pu517_445: c_unsorted,A__questionmark_o1u516_446: $int,A__questionmark_s1u515_447: $int,A__questionmark_o2u514_448: $int,A__questionmark_s2u513_449: $int] :
    ? [A__questionmark_v_0_232: c_sorted,A__questionmark_v_1_233: c_sorted] :
      ( ( A__questionmark_v_0_232 = c_sort(memory(A__questionmark_t1u0_443,bitvector),A__questionmark_mu518_444) )
      & ( A__questionmark_v_1_233 = c_sort(pointer(A__questionmark_t1u0_443),A__questionmark_pu517_445) )
      & ( ( $sum(A__questionmark_o1u516_446,A__questionmark_s1u515_447) = A__questionmark_o2u514_448 )
       => ( c_sort(bitvector,concat_bitvector(c_sort(bitvector,select_bytes(A__questionmark_v_0_232,A__questionmark_v_1_233,A__questionmark_o1u516_446,A__questionmark_s1u515_447)),c_sort(bitvector,select_bytes(A__questionmark_v_0_232,A__questionmark_v_1_233,A__questionmark_o2u514_448,A__questionmark_s2u513_449)))) = c_sort(bitvector,select_bytes(A__questionmark_v_0_232,A__questionmark_v_1_233,A__questionmark_o1u516_446,$sum(A__questionmark_s1u515_447,A__questionmark_s2u513_449))) ) ) ) ).

tff(formula_132,axiom,
    int_of_tag(c_sort(tag_id(smtlib____anonstruct_T_CompositionPage_1),smtlib____anonstruct_T_CompositionPage_1_tag)) = 1 ).

tff(formula_133,axiom,
    ! [A__questionmark_xu539_450: c_unsorted] :
    ? [A__questionmark_v_0_234: c_type] :
      ( ( A__questionmark_v_0_234 = pointer(smtlib____anonstruct_T_CompositionPage_1) )
      & ? [A__questionmark_v_1_235: c_sorted] :
          ( ( A__questionmark_v_1_235 = c_sort(A__questionmark_v_0_234,A__questionmark_xu539_450) )
          & ( c_sort(A__questionmark_v_0_234,smtlib____anonstruct_T_CompositionPage_1_of_bitvector(c_sort(bitvector,bitvector_of___anonstruct_T_CompositionPage_1(A__questionmark_v_1_235)))) = A__questionmark_v_1_235 ) ) ) ).

tff(formula_134,axiom,
    ! [A__questionmark_pu540_451: c_unsorted] :
    ? [A__questionmark_v_0_236: c_type] :
      ( ( A__questionmark_v_0_236 = pointer(smtlib____anonstruct_T_CompositionPage_1) )
      & ? [A__questionmark_v_1_237: c_sorted] :
          ( ( A__questionmark_v_1_237 = c_sort(A__questionmark_v_0_236,A__questionmark_pu540_451) )
          & ( A__questionmark_v_1_237 = c_sort(A__questionmark_v_0_236,smtlib____anonstruct_T_CompositionPage_1_of_pointer_address(c_sort(pointer(c_unit),pointer_address(A__questionmark_v_1_237)))) ) ) ) ).

tff(formula_135,axiom,
    ? [A__questionmark_v_0_238: c_type] :
      ( ( A__questionmark_v_0_238 = tag_id(smtlib____anonstruct_T_CompositionPage_1) )
      & parenttag(c_sort(A__questionmark_v_0_238,smtlib____anonstruct_T_CompositionPage_1_tag),c_sort(A__questionmark_v_0_238,bottom_tag)) ) ).

tff(formula_136,axiom,
    ! [A__questionmark_xu542_452: c_unsorted,A__questionmark_uuanonstructuTuCompositionPageu1utagutableu541_453: c_unsorted] : instanceof(c_sort(tag_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_uuanonstructuTuCompositionPageu1utagutableu541_453),c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_xu542_452),c_sort(tag_id(smtlib____anonstruct_T_CompositionPage_1),smtlib____anonstruct_T_CompositionPage_1_tag)) ).

tff(formula_137,axiom,
    ! [A__questionmark_xu543_454: c_unsorted] :
    ? [A__questionmark_v_0_239: c_sorted] :
      ( ( A__questionmark_v_0_239 = c_sort(bitvector,A__questionmark_xu543_454) )
      & ( c_sort(bitvector,bitvector_of___anonstruct_T_CompositionPage_1(c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),smtlib____anonstruct_T_CompositionPage_1_of_bitvector(A__questionmark_v_0_239)))) = A__questionmark_v_0_239 ) ) ).

tff(formula_138,axiom,
    ! [A__questionmark_xu544_455: c_unsorted] :
    ? [A__questionmark_v_0_240: c_sorted] :
      ( ( A__questionmark_v_0_240 = c_sort(bitvector,A__questionmark_xu544_455) )
      & ( c_sort(bitvector,bitvector_of_char_P(c_sort(pointer(char_P),char_P_of_bitvector(A__questionmark_v_0_240)))) = A__questionmark_v_0_240 ) ) ).

tff(formula_139,axiom,
    ! [A__questionmark_xu545_456: c_unsorted] :
    ? [A__questionmark_v_0_241: c_sorted] :
      ( ( A__questionmark_v_0_241 = c_sort(bitvector,A__questionmark_xu545_456) )
      & ( c_sort(bitvector,bitvector_of_char__x__1__P(c_sort(pointer(char__x__1__P),char__x__1__P_of_bitvector(A__questionmark_v_0_241)))) = A__questionmark_v_0_241 ) ) ).

tff(formula_140,axiom,
    ! [A__questionmark_xu546_457: c_unsorted] :
    ? [A__questionmark_v_0_242: c_sorted] :
      ( ( A__questionmark_v_0_242 = c_sort(bitvector,A__questionmark_xu546_457) )
      & ( c_sort(bitvector,bitvector_of_int8(c_sort(int8,int8_of_bitvector(A__questionmark_v_0_242)))) = A__questionmark_v_0_242 ) ) ).

tff(formula_141,axiom,
    ! [A__questionmark_xu547_458: c_unsorted] :
    ? [A__questionmark_v_0_243: c_sorted] :
      ( ( A__questionmark_v_0_243 = c_sort(bitvector,A__questionmark_xu547_458) )
      & ( c_sort(bitvector,bitvector_of_void_P(c_sort(pointer(void_P),void_P_of_bitvector(A__questionmark_v_0_243)))) = A__questionmark_v_0_243 ) ) ).

tff(formula_142,axiom,
    int_of_tag(c_sort(tag_id(char_P),char_P_tag)) = 1 ).

tff(formula_143,axiom,
    ! [A__questionmark_xu548_459: c_unsorted] :
    ? [A__questionmark_v_0_244: c_type] :
      ( ( A__questionmark_v_0_244 = pointer(char_P) )
      & ? [A__questionmark_v_1_245: c_sorted] :
          ( ( A__questionmark_v_1_245 = c_sort(A__questionmark_v_0_244,A__questionmark_xu548_459) )
          & ( c_sort(A__questionmark_v_0_244,char_P_of_bitvector(c_sort(bitvector,bitvector_of_char_P(A__questionmark_v_1_245)))) = A__questionmark_v_1_245 ) ) ) ).

tff(formula_144,axiom,
    ! [A__questionmark_pu549_460: c_unsorted] :
    ? [A__questionmark_v_0_246: c_type] :
      ( ( A__questionmark_v_0_246 = pointer(char_P) )
      & ? [A__questionmark_v_1_247: c_sorted] :
          ( ( A__questionmark_v_1_247 = c_sort(A__questionmark_v_0_246,A__questionmark_pu549_460) )
          & ( A__questionmark_v_1_247 = c_sort(A__questionmark_v_0_246,char_P_of_pointer_address(c_sort(pointer(c_unit),pointer_address(A__questionmark_v_1_247)))) ) ) ) ).

tff(formula_145,axiom,
    ? [A__questionmark_v_0_248: c_type] :
      ( ( A__questionmark_v_0_248 = tag_id(char_P) )
      & parenttag(c_sort(A__questionmark_v_0_248,char_P_tag),c_sort(A__questionmark_v_0_248,bottom_tag)) ) ).

tff(formula_146,axiom,
    ! [A__questionmark_xu551_461: c_unsorted,A__questionmark_charuPutagutableu550_462: c_unsorted] : instanceof(c_sort(tag_table(char_P),A__questionmark_charuPutagutableu550_462),c_sort(pointer(char_P),A__questionmark_xu551_461),c_sort(tag_id(char_P),char_P_tag)) ).

tff(formula_147,axiom,
    int_of_tag(c_sort(tag_id(char__x__1__P),char__x__1__P_tag)) = 1 ).

tff(formula_148,axiom,
    ! [A__questionmark_xu552_463: c_unsorted] :
    ? [A__questionmark_v_0_249: c_type] :
      ( ( A__questionmark_v_0_249 = pointer(char__x__1__P) )
      & ? [A__questionmark_v_1_250: c_sorted] :
          ( ( A__questionmark_v_1_250 = c_sort(A__questionmark_v_0_249,A__questionmark_xu552_463) )
          & ( c_sort(A__questionmark_v_0_249,char__x__1__P_of_bitvector(c_sort(bitvector,bitvector_of_char__x__1__P(A__questionmark_v_1_250)))) = A__questionmark_v_1_250 ) ) ) ).

tff(formula_149,axiom,
    ! [A__questionmark_pu553_464: c_unsorted] :
    ? [A__questionmark_v_0_251: c_type] :
      ( ( A__questionmark_v_0_251 = pointer(char__x__1__P) )
      & ? [A__questionmark_v_1_252: c_sorted] :
          ( ( A__questionmark_v_1_252 = c_sort(A__questionmark_v_0_251,A__questionmark_pu553_464) )
          & ( A__questionmark_v_1_252 = c_sort(A__questionmark_v_0_251,char__x__1__P_of_pointer_address(c_sort(pointer(c_unit),pointer_address(A__questionmark_v_1_252)))) ) ) ) ).

tff(formula_150,axiom,
    ? [A__questionmark_v_0_253: c_type] :
      ( ( A__questionmark_v_0_253 = tag_id(char__x__1__P) )
      & parenttag(c_sort(A__questionmark_v_0_253,char__x__1__P_tag),c_sort(A__questionmark_v_0_253,bottom_tag)) ) ).

tff(formula_151,axiom,
    ! [A__questionmark_xu555_465: c_unsorted,A__questionmark_charuuxuu1uuPutagutableu554_466: c_unsorted] : instanceof(c_sort(tag_table(char__x__1__P),A__questionmark_charuuxuu1uuPutagutableu554_466),c_sort(pointer(char__x__1__P),A__questionmark_xu555_465),c_sort(tag_id(char__x__1__P),char__x__1__P_tag)) ).

tff(formula_152,axiom,
    ! [A__questionmark_xu0_467: c_unsorted,A__questionmark_yu0_468: c_unsorted] :
    ? [A__questionmark_v_0_254: c_sorted,A__questionmark_v_1_255: c_sorted] :
      ( ( A__questionmark_v_0_254 = c_sort(int8,A__questionmark_xu0_467) )
      & ( A__questionmark_v_1_255 = c_sort(int8,A__questionmark_yu0_468) )
      & ( eq_int8(A__questionmark_v_0_254,A__questionmark_v_1_255)
      <=> ( integer_of_int8(A__questionmark_v_0_254) = integer_of_int8(A__questionmark_v_1_255) ) ) ) ).

tff(formula_153,axiom,
    ! [A__questionmark_xu556_469: $int] :
      ( ( $lesseq($uminus(128),A__questionmark_xu556_469)
        & $lesseq(A__questionmark_xu556_469,127) )
     => ( integer_of_int8(c_sort(int8,int8_of_integer(A__questionmark_xu556_469))) = A__questionmark_xu556_469 ) ) ).

tff(formula_154,axiom,
    ! [A__questionmark_xu557_470: c_unsorted] :
    ? [A__questionmark_v_0_256: c_sorted] :
      ( ( A__questionmark_v_0_256 = c_sort(int8,A__questionmark_xu557_470) )
      & eq_int8(c_sort(int8,int8_of_bitvector(c_sort(bitvector,bitvector_of_int8(A__questionmark_v_0_256)))),A__questionmark_v_0_256) ) ).

tff(formula_155,axiom,
    ! [A__questionmark_xu558_471: c_unsorted] :
    ? [A__questionmark_v_0_257: $int] :
      ( ( A__questionmark_v_0_257 = integer_of_int8(c_sort(int8,A__questionmark_xu558_471)) )
      & $lesseq($uminus(128),A__questionmark_v_0_257)
      & $lesseq(A__questionmark_v_0_257,127) ) ).

tff(formula_156,axiom,
    ! [A__questionmark_pu0_472: c_unsorted,A__questionmark_au0_473: $int,A__questionmark_charuPuallocutableu0_474: c_unsorted] :
    ? [A__questionmark_v_1_258: c_sorted,A__questionmark_v_0_259: c_sorted] :
      ( ( A__questionmark_v_1_258 = c_sort(pointer(char_P),A__questionmark_pu0_472) )
      & ( A__questionmark_v_0_259 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_474) )
      & ( left_valid_struct_char_P(A__questionmark_v_1_258,A__questionmark_au0_473,A__questionmark_v_0_259)
      <=> $lesseq(offset_min(A__questionmark_v_0_259,A__questionmark_v_1_258),A__questionmark_au0_473) ) ) ).

tff(formula_157,axiom,
    ! [A__questionmark_pu0_475: c_unsorted,A__questionmark_au0_476: $int,A__questionmark_charuPuallocutableu0_477: c_unsorted,A__questionmark_charuuxuu1uuPuallocutableu0_478: c_unsorted,A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_479: c_unsorted] :
    ? [A__questionmark_v_2_260: c_type,A__questionmark_v_1_261: c_sorted,A__questionmark_v_4_262: c_sorted,A__questionmark_v_0_263: c_sorted] :
      ( ( A__questionmark_v_2_260 = pointer(char_P) )
      & ( A__questionmark_v_1_261 = c_sort(pointer(char__x__1__P),A__questionmark_pu0_475) )
      & ( A__questionmark_v_4_262 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_477) )
      & ( A__questionmark_v_0_263 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_478) )
      & ? [A__questionmark_v_3_264: c_sorted] :
          ( ( A__questionmark_v_3_264 = c_sort(memory(char__x__1__P,A__questionmark_v_2_260),A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_479) )
          & ( left_valid_struct_char__x__1__P(A__questionmark_v_1_261,A__questionmark_au0_476,A__questionmark_v_4_262,A__questionmark_v_0_263,A__questionmark_v_3_264)
          <=> ( $lesseq(offset_min(A__questionmark_v_0_263,A__questionmark_v_1_261),A__questionmark_au0_476)
              & left_valid_struct_char_P(c_sort(A__questionmark_v_2_260,smtlib__select(A__questionmark_v_3_264,A__questionmark_v_1_261)),0,A__questionmark_v_4_262) ) ) ) ) ).

tff(formula_158,axiom,
    ! [A__questionmark_pu0_480: c_unsorted,A__questionmark_au0_481: $int,A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_482: c_unsorted,A__questionmark_charuPuallocutableu0_483: c_unsorted,A__questionmark_charuuxuu1uuPuallocutableu0_484: c_unsorted,A__questionmark_uuanonstructuTuCompositionPageu1uTexteu0_485: c_unsorted,A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_486: c_unsorted] :
    ? [A__questionmark_v_2_265: c_type,A__questionmark_v_1_266: c_sorted,A__questionmark_v_0_267: c_sorted,A__questionmark_v_4_268: c_sorted,A__questionmark_v_5_269: c_sorted] :
      ( ( A__questionmark_v_2_265 = pointer(char__x__1__P) )
      & ( A__questionmark_v_1_266 = c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_pu0_480) )
      & ( A__questionmark_v_0_267 = c_sort(alloc_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_482) )
      & ( A__questionmark_v_4_268 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_483) )
      & ( A__questionmark_v_5_269 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_484) )
      & ? [A__questionmark_v_3_270: c_sorted,A__questionmark_v_6_271: c_sorted] :
          ( ( A__questionmark_v_3_270 = c_sort(memory(smtlib____anonstruct_T_CompositionPage_1,A__questionmark_v_2_265),A__questionmark_uuanonstructuTuCompositionPageu1uTexteu0_485) )
          & ( A__questionmark_v_6_271 = c_sort(memory(char__x__1__P,pointer(char_P)),A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_486) )
          & ( left_valid_struct___anonstruct_T_CompositionPage_1(A__questionmark_v_1_266,A__questionmark_au0_481,A__questionmark_v_0_267,A__questionmark_v_4_268,A__questionmark_v_5_269,A__questionmark_v_3_270,A__questionmark_v_6_271)
          <=> ( $lesseq(offset_min(A__questionmark_v_0_267,A__questionmark_v_1_266),A__questionmark_au0_481)
              & left_valid_struct_char__x__1__P(c_sort(A__questionmark_v_2_265,smtlib__select(A__questionmark_v_3_270,A__questionmark_v_1_266)),0,A__questionmark_v_4_268,A__questionmark_v_5_269,A__questionmark_v_6_271) ) ) ) ) ).

tff(formula_159,axiom,
    ! [A__questionmark_pu0_487: c_unsorted,A__questionmark_au0_488: $int,A__questionmark_voiduPuallocutableu0_489: c_unsorted] :
    ? [A__questionmark_v_1_272: c_sorted,A__questionmark_v_0_273: c_sorted] :
      ( ( A__questionmark_v_1_272 = c_sort(pointer(void_P),A__questionmark_pu0_487) )
      & ( A__questionmark_v_0_273 = c_sort(alloc_table(void_P),A__questionmark_voiduPuallocutableu0_489) )
      & ( left_valid_struct_void_P(A__questionmark_v_1_272,A__questionmark_au0_488,A__questionmark_v_0_273)
      <=> $lesseq(offset_min(A__questionmark_v_0_273,A__questionmark_v_1_272),A__questionmark_au0_488) ) ) ).

tff(formula_160,axiom,
    ! [A__questionmark_pu559_490: c_unsorted] :
    ? [A__questionmark_v_0_274: c_type] :
      ( ( A__questionmark_v_0_274 = pointer(c_unit) )
      & ? [A__questionmark_v_1_275: c_sorted] :
          ( ( A__questionmark_v_1_275 = c_sort(A__questionmark_v_0_274,A__questionmark_pu559_490) )
          & ( A__questionmark_v_1_275 = c_sort(A__questionmark_v_0_274,pointer_address(c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),smtlib____anonstruct_T_CompositionPage_1_of_pointer_address(A__questionmark_v_1_275)))) ) ) ) ).

tff(formula_161,axiom,
    ! [A__questionmark_pu560_491: c_unsorted] :
    ? [A__questionmark_v_0_276: c_type] :
      ( ( A__questionmark_v_0_276 = pointer(c_unit) )
      & ? [A__questionmark_v_1_277: c_sorted] :
          ( ( A__questionmark_v_1_277 = c_sort(A__questionmark_v_0_276,A__questionmark_pu560_491) )
          & ( A__questionmark_v_1_277 = c_sort(A__questionmark_v_0_276,pointer_address(c_sort(pointer(char_P),char_P_of_pointer_address(A__questionmark_v_1_277)))) ) ) ) ).

tff(formula_162,axiom,
    ! [A__questionmark_pu561_492: c_unsorted] :
    ? [A__questionmark_v_0_278: c_type] :
      ( ( A__questionmark_v_0_278 = pointer(c_unit) )
      & ? [A__questionmark_v_1_279: c_sorted] :
          ( ( A__questionmark_v_1_279 = c_sort(A__questionmark_v_0_278,A__questionmark_pu561_492) )
          & ( A__questionmark_v_1_279 = c_sort(A__questionmark_v_0_278,pointer_address(c_sort(pointer(char__x__1__P),char__x__1__P_of_pointer_address(A__questionmark_v_1_279)))) ) ) ) ).

tff(formula_163,axiom,
    ! [A__questionmark_pu562_493: c_unsorted] :
    ? [A__questionmark_v_0_280: c_type] :
      ( ( A__questionmark_v_0_280 = pointer(c_unit) )
      & ? [A__questionmark_v_1_281: c_sorted] :
          ( ( A__questionmark_v_1_281 = c_sort(A__questionmark_v_0_280,A__questionmark_pu562_493) )
          & ( A__questionmark_v_1_281 = c_sort(A__questionmark_v_0_280,pointer_address(c_sort(pointer(void_P),void_P_of_pointer_address(A__questionmark_v_1_281)))) ) ) ) ).

tff(formula_164,axiom,
    ! [A__questionmark_pu0_494: c_unsorted,A__questionmark_bu0_495: $int,A__questionmark_charuPuallocutableu0_496: c_unsorted] :
    ? [A__questionmark_v_1_282: c_sorted,A__questionmark_v_0_283: c_sorted] :
      ( ( A__questionmark_v_1_282 = c_sort(pointer(char_P),A__questionmark_pu0_494) )
      & ( A__questionmark_v_0_283 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_496) )
      & ( right_valid_struct_char_P(A__questionmark_v_1_282,A__questionmark_bu0_495,A__questionmark_v_0_283)
      <=> $greatereq(offset_max(A__questionmark_v_0_283,A__questionmark_v_1_282),A__questionmark_bu0_495) ) ) ).

tff(formula_165,axiom,
    ! [A__questionmark_pu0_497: c_unsorted,A__questionmark_bu0_498: $int,A__questionmark_charuPuallocutableu0_499: c_unsorted,A__questionmark_charuuxuu1uuPuallocutableu0_500: c_unsorted,A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_501: c_unsorted] :
    ? [A__questionmark_v_2_284: c_type,A__questionmark_v_1_285: c_sorted,A__questionmark_v_4_286: c_sorted,A__questionmark_v_0_287: c_sorted] :
      ( ( A__questionmark_v_2_284 = pointer(char_P) )
      & ( A__questionmark_v_1_285 = c_sort(pointer(char__x__1__P),A__questionmark_pu0_497) )
      & ( A__questionmark_v_4_286 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_499) )
      & ( A__questionmark_v_0_287 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_500) )
      & ? [A__questionmark_v_3_288: c_sorted] :
          ( ( A__questionmark_v_3_288 = c_sort(memory(char__x__1__P,A__questionmark_v_2_284),A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_501) )
          & ( right_valid_struct_char__x__1__P(A__questionmark_v_1_285,A__questionmark_bu0_498,A__questionmark_v_4_286,A__questionmark_v_0_287,A__questionmark_v_3_288)
          <=> ( $greatereq(offset_max(A__questionmark_v_0_287,A__questionmark_v_1_285),A__questionmark_bu0_498)
              & right_valid_struct_char_P(c_sort(A__questionmark_v_2_284,smtlib__select(A__questionmark_v_3_288,A__questionmark_v_1_285)),9,A__questionmark_v_4_286) ) ) ) ) ).

tff(formula_166,axiom,
    ! [A__questionmark_pu0_502: c_unsorted,A__questionmark_bu0_503: $int,A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_504: c_unsorted,A__questionmark_charuPuallocutableu0_505: c_unsorted,A__questionmark_charuuxuu1uuPuallocutableu0_506: c_unsorted,A__questionmark_uuanonstructuTuCompositionPageu1uTexteu0_507: c_unsorted,A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_508: c_unsorted] :
    ? [A__questionmark_v_2_289: c_type,A__questionmark_v_1_290: c_sorted,A__questionmark_v_0_291: c_sorted,A__questionmark_v_4_292: c_sorted,A__questionmark_v_5_293: c_sorted] :
      ( ( A__questionmark_v_2_289 = pointer(char__x__1__P) )
      & ( A__questionmark_v_1_290 = c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_pu0_502) )
      & ( A__questionmark_v_0_291 = c_sort(alloc_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_504) )
      & ( A__questionmark_v_4_292 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_505) )
      & ( A__questionmark_v_5_293 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_506) )
      & ? [A__questionmark_v_3_294: c_sorted,A__questionmark_v_6_295: c_sorted] :
          ( ( A__questionmark_v_3_294 = c_sort(memory(smtlib____anonstruct_T_CompositionPage_1,A__questionmark_v_2_289),A__questionmark_uuanonstructuTuCompositionPageu1uTexteu0_507) )
          & ( A__questionmark_v_6_295 = c_sort(memory(char__x__1__P,pointer(char_P)),A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_508) )
          & ( right_valid_struct___anonstruct_T_CompositionPage_1(A__questionmark_v_1_290,A__questionmark_bu0_503,A__questionmark_v_0_291,A__questionmark_v_4_292,A__questionmark_v_5_293,A__questionmark_v_3_294,A__questionmark_v_6_295)
          <=> ( $greatereq(offset_max(A__questionmark_v_0_291,A__questionmark_v_1_290),A__questionmark_bu0_503)
              & right_valid_struct_char__x__1__P(c_sort(A__questionmark_v_2_289,smtlib__select(A__questionmark_v_3_294,A__questionmark_v_1_290)),9,A__questionmark_v_4_292,A__questionmark_v_5_293,A__questionmark_v_6_295) ) ) ) ) ).

tff(formula_167,axiom,
    ! [A__questionmark_pu0_509: c_unsorted,A__questionmark_bu0_510: $int,A__questionmark_voiduPuallocutableu0_511: c_unsorted] :
    ? [A__questionmark_v_1_296: c_sorted,A__questionmark_v_0_297: c_sorted] :
      ( ( A__questionmark_v_1_296 = c_sort(pointer(void_P),A__questionmark_pu0_509) )
      & ( A__questionmark_v_0_297 = c_sort(alloc_table(void_P),A__questionmark_voiduPuallocutableu0_511) )
      & ( right_valid_struct_void_P(A__questionmark_v_1_296,A__questionmark_bu0_510,A__questionmark_v_0_297)
      <=> $greatereq(offset_max(A__questionmark_v_0_297,A__questionmark_v_1_296),A__questionmark_bu0_510) ) ) ).

tff(formula_168,axiom,
    ! [A__questionmark_pu0_512: c_unsorted,A__questionmark_au0_513: $int,A__questionmark_bu0_514: $int,A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_515: c_unsorted] :
    ? [A__questionmark_v_1_298: c_sorted,A__questionmark_v_0_299: c_sorted] :
      ( ( A__questionmark_v_1_298 = c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_pu0_512) )
      & ( A__questionmark_v_0_299 = c_sort(alloc_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_515) )
      & ( strict_valid_root___anonstruct_T_CompositionPage_1(A__questionmark_v_1_298,A__questionmark_au0_513,A__questionmark_bu0_514,A__questionmark_v_0_299)
      <=> ( ( offset_min(A__questionmark_v_0_299,A__questionmark_v_1_298) = A__questionmark_au0_513 )
          & ( offset_max(A__questionmark_v_0_299,A__questionmark_v_1_298) = A__questionmark_bu0_514 ) ) ) ) ).

tff(formula_169,axiom,
    ! [A__questionmark_pu0_516: c_unsorted,A__questionmark_au0_517: $int,A__questionmark_bu0_518: $int,A__questionmark_charuPuallocutableu0_519: c_unsorted] :
    ? [A__questionmark_v_1_300: c_sorted,A__questionmark_v_0_301: c_sorted] :
      ( ( A__questionmark_v_1_300 = c_sort(pointer(char_P),A__questionmark_pu0_516) )
      & ( A__questionmark_v_0_301 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_519) )
      & ( strict_valid_root_char_P(A__questionmark_v_1_300,A__questionmark_au0_517,A__questionmark_bu0_518,A__questionmark_v_0_301)
      <=> ( ( offset_min(A__questionmark_v_0_301,A__questionmark_v_1_300) = A__questionmark_au0_517 )
          & ( offset_max(A__questionmark_v_0_301,A__questionmark_v_1_300) = A__questionmark_bu0_518 ) ) ) ) ).

tff(formula_170,axiom,
    ! [A__questionmark_pu0_520: c_unsorted,A__questionmark_au0_521: $int,A__questionmark_bu0_522: $int,A__questionmark_charuuxuu1uuPuallocutableu0_523: c_unsorted] :
    ? [A__questionmark_v_1_302: c_sorted,A__questionmark_v_0_303: c_sorted] :
      ( ( A__questionmark_v_1_302 = c_sort(pointer(char__x__1__P),A__questionmark_pu0_520) )
      & ( A__questionmark_v_0_303 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_523) )
      & ( strict_valid_root_char__x__1__P(A__questionmark_v_1_302,A__questionmark_au0_521,A__questionmark_bu0_522,A__questionmark_v_0_303)
      <=> ( ( offset_min(A__questionmark_v_0_303,A__questionmark_v_1_302) = A__questionmark_au0_521 )
          & ( offset_max(A__questionmark_v_0_303,A__questionmark_v_1_302) = A__questionmark_bu0_522 ) ) ) ) ).

tff(formula_171,axiom,
    ! [A__questionmark_pu0_524: c_unsorted,A__questionmark_au0_525: $int,A__questionmark_bu0_526: $int,A__questionmark_voiduPuallocutableu0_527: c_unsorted] :
    ? [A__questionmark_v_1_304: c_sorted,A__questionmark_v_0_305: c_sorted] :
      ( ( A__questionmark_v_1_304 = c_sort(pointer(void_P),A__questionmark_pu0_524) )
      & ( A__questionmark_v_0_305 = c_sort(alloc_table(void_P),A__questionmark_voiduPuallocutableu0_527) )
      & ( strict_valid_root_void_P(A__questionmark_v_1_304,A__questionmark_au0_525,A__questionmark_bu0_526,A__questionmark_v_0_305)
      <=> ( ( offset_min(A__questionmark_v_0_305,A__questionmark_v_1_304) = A__questionmark_au0_525 )
          & ( offset_max(A__questionmark_v_0_305,A__questionmark_v_1_304) = A__questionmark_bu0_526 ) ) ) ) ).

tff(formula_172,axiom,
    ! [A__questionmark_pu0_528: c_unsorted,A__questionmark_au0_529: $int,A__questionmark_bu0_530: $int,A__questionmark_charuPuallocutableu0_531: c_unsorted] :
    ? [A__questionmark_v_1_306: c_sorted,A__questionmark_v_0_307: c_sorted] :
      ( ( A__questionmark_v_1_306 = c_sort(pointer(char_P),A__questionmark_pu0_528) )
      & ( A__questionmark_v_0_307 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_531) )
      & ( strict_valid_struct_char_P(A__questionmark_v_1_306,A__questionmark_au0_529,A__questionmark_bu0_530,A__questionmark_v_0_307)
      <=> ( ( offset_min(A__questionmark_v_0_307,A__questionmark_v_1_306) = A__questionmark_au0_529 )
          & ( offset_max(A__questionmark_v_0_307,A__questionmark_v_1_306) = A__questionmark_bu0_530 ) ) ) ) ).

tff(formula_173,axiom,
    ! [A__questionmark_pu0_532: c_unsorted,A__questionmark_au0_533: $int,A__questionmark_bu0_534: $int,A__questionmark_charuPuallocutableu0_535: c_unsorted,A__questionmark_charuuxuu1uuPuallocutableu0_536: c_unsorted,A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_537: c_unsorted] :
    ? [A__questionmark_v_2_308: c_type,A__questionmark_v_1_309: c_sorted,A__questionmark_v_4_310: c_sorted,A__questionmark_v_0_311: c_sorted] :
      ( ( A__questionmark_v_2_308 = pointer(char_P) )
      & ( A__questionmark_v_1_309 = c_sort(pointer(char__x__1__P),A__questionmark_pu0_532) )
      & ( A__questionmark_v_4_310 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_535) )
      & ( A__questionmark_v_0_311 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_536) )
      & ? [A__questionmark_v_3_312: c_sorted] :
          ( ( A__questionmark_v_3_312 = c_sort(memory(char__x__1__P,A__questionmark_v_2_308),A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_537) )
          & ( strict_valid_struct_char__x__1__P(A__questionmark_v_1_309,A__questionmark_au0_533,A__questionmark_bu0_534,A__questionmark_v_4_310,A__questionmark_v_0_311,A__questionmark_v_3_312)
          <=> ( ( offset_min(A__questionmark_v_0_311,A__questionmark_v_1_309) = A__questionmark_au0_533 )
              & ( offset_max(A__questionmark_v_0_311,A__questionmark_v_1_309) = A__questionmark_bu0_534 )
              & strict_valid_struct_char_P(c_sort(A__questionmark_v_2_308,smtlib__select(A__questionmark_v_3_312,A__questionmark_v_1_309)),0,9,A__questionmark_v_4_310) ) ) ) ) ).

tff(formula_174,axiom,
    ! [A__questionmark_pu0_538: c_unsorted,A__questionmark_au0_539: $int,A__questionmark_bu0_540: $int,A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_541: c_unsorted,A__questionmark_charuPuallocutableu0_542: c_unsorted,A__questionmark_charuuxuu1uuPuallocutableu0_543: c_unsorted,A__questionmark_uuanonstructuTuCompositionPageu1uTexteu0_544: c_unsorted,A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_545: c_unsorted] :
    ? [A__questionmark_v_2_313: c_type,A__questionmark_v_1_314: c_sorted,A__questionmark_v_0_315: c_sorted,A__questionmark_v_4_316: c_sorted,A__questionmark_v_5_317: c_sorted] :
      ( ( A__questionmark_v_2_313 = pointer(char__x__1__P) )
      & ( A__questionmark_v_1_314 = c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_pu0_538) )
      & ( A__questionmark_v_0_315 = c_sort(alloc_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_541) )
      & ( A__questionmark_v_4_316 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_542) )
      & ( A__questionmark_v_5_317 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_543) )
      & ? [A__questionmark_v_3_318: c_sorted,A__questionmark_v_6_319: c_sorted] :
          ( ( A__questionmark_v_3_318 = c_sort(memory(smtlib____anonstruct_T_CompositionPage_1,A__questionmark_v_2_313),A__questionmark_uuanonstructuTuCompositionPageu1uTexteu0_544) )
          & ( A__questionmark_v_6_319 = c_sort(memory(char__x__1__P,pointer(char_P)),A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_545) )
          & ( strict_valid_struct___anonstruct_T_CompositionPage_1(A__questionmark_v_1_314,A__questionmark_au0_539,A__questionmark_bu0_540,A__questionmark_v_0_315,A__questionmark_v_4_316,A__questionmark_v_5_317,A__questionmark_v_3_318,A__questionmark_v_6_319)
          <=> ( ( offset_min(A__questionmark_v_0_315,A__questionmark_v_1_314) = A__questionmark_au0_539 )
              & ( offset_max(A__questionmark_v_0_315,A__questionmark_v_1_314) = A__questionmark_bu0_540 )
              & strict_valid_struct_char__x__1__P(c_sort(A__questionmark_v_2_313,smtlib__select(A__questionmark_v_3_318,A__questionmark_v_1_314)),0,9,A__questionmark_v_4_316,A__questionmark_v_5_317,A__questionmark_v_6_319) ) ) ) ) ).

tff(formula_175,axiom,
    ! [A__questionmark_pu0_546: c_unsorted,A__questionmark_au0_547: $int,A__questionmark_bu0_548: $int,A__questionmark_voiduPuallocutableu0_549: c_unsorted] :
    ? [A__questionmark_v_1_320: c_sorted,A__questionmark_v_0_321: c_sorted] :
      ( ( A__questionmark_v_1_320 = c_sort(pointer(void_P),A__questionmark_pu0_546) )
      & ( A__questionmark_v_0_321 = c_sort(alloc_table(void_P),A__questionmark_voiduPuallocutableu0_549) )
      & ( strict_valid_struct_void_P(A__questionmark_v_1_320,A__questionmark_au0_547,A__questionmark_bu0_548,A__questionmark_v_0_321)
      <=> ( ( offset_min(A__questionmark_v_0_321,A__questionmark_v_1_320) = A__questionmark_au0_547 )
          & ( offset_max(A__questionmark_v_0_321,A__questionmark_v_1_320) = A__questionmark_bu0_548 ) ) ) ) ).

tff(formula_176,axiom,
    ! [A__questionmark_uuanonstructuTuCompositionPageu1uPageu1uallocutableu0_550: c_unsorted] :
    ? [A__questionmark_v_0_322: c_sorted,A__questionmark_v_1_323: c_sorted] :
      ( ( A__questionmark_v_0_322 = c_sort(alloc_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_uuanonstructuTuCompositionPageu1uPageu1uallocutableu0_550) )
      & ( A__questionmark_v_1_323 = c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),'Page') )
      & ( valid_Page(A__questionmark_v_0_322)
      <=> ( $lesseq(offset_min(A__questionmark_v_0_322,A__questionmark_v_1_323),0)
          & $greatereq(offset_max(A__questionmark_v_0_322,A__questionmark_v_1_323),0) ) ) ) ).

tff(formula_177,axiom,
    ! [A__questionmark_pu0_551: c_unsorted,A__questionmark_au0_552: $int,A__questionmark_bu0_553: $int,A__questionmark_bitvectoruallocutableu0_554: c_unsorted] :
    ? [A__questionmark_v_1_324: c_sorted,A__questionmark_v_0_325: c_sorted] :
      ( ( A__questionmark_v_1_324 = c_sort(pointer(c_unit),A__questionmark_pu0_551) )
      & ( A__questionmark_v_0_325 = c_sort(alloc_table(c_unit),A__questionmark_bitvectoruallocutableu0_554) )
      & ( valid_bitvector_struct___anonstruct_T_CompositionPage_1(A__questionmark_v_1_324,A__questionmark_au0_552,A__questionmark_bu0_553,A__questionmark_v_0_325)
      <=> ( ( offset_min(A__questionmark_v_0_325,A__questionmark_v_1_324) = A__questionmark_au0_552 )
          & ( offset_max(A__questionmark_v_0_325,A__questionmark_v_1_324) = A__questionmark_bu0_553 ) ) ) ) ).

tff(formula_178,axiom,
    ! [A__questionmark_pu0_555: c_unsorted,A__questionmark_au0_556: $int,A__questionmark_bu0_557: $int,A__questionmark_bitvectoruallocutableu0_558: c_unsorted] :
    ? [A__questionmark_v_1_326: c_sorted,A__questionmark_v_0_327: c_sorted] :
      ( ( A__questionmark_v_1_326 = c_sort(pointer(c_unit),A__questionmark_pu0_555) )
      & ( A__questionmark_v_0_327 = c_sort(alloc_table(c_unit),A__questionmark_bitvectoruallocutableu0_558) )
      & ( valid_bitvector_struct_char_P(A__questionmark_v_1_326,A__questionmark_au0_556,A__questionmark_bu0_557,A__questionmark_v_0_327)
      <=> ( ( offset_min(A__questionmark_v_0_327,A__questionmark_v_1_326) = A__questionmark_au0_556 )
          & ( offset_max(A__questionmark_v_0_327,A__questionmark_v_1_326) = A__questionmark_bu0_557 ) ) ) ) ).

tff(formula_179,axiom,
    ! [A__questionmark_pu0_559: c_unsorted,A__questionmark_au0_560: $int,A__questionmark_bu0_561: $int,A__questionmark_bitvectoruallocutableu0_562: c_unsorted] :
    ? [A__questionmark_v_1_328: c_sorted,A__questionmark_v_0_329: c_sorted] :
      ( ( A__questionmark_v_1_328 = c_sort(pointer(c_unit),A__questionmark_pu0_559) )
      & ( A__questionmark_v_0_329 = c_sort(alloc_table(c_unit),A__questionmark_bitvectoruallocutableu0_562) )
      & ( valid_bitvector_struct_char__x__1__P(A__questionmark_v_1_328,A__questionmark_au0_560,A__questionmark_bu0_561,A__questionmark_v_0_329)
      <=> ( ( offset_min(A__questionmark_v_0_329,A__questionmark_v_1_328) = A__questionmark_au0_560 )
          & ( offset_max(A__questionmark_v_0_329,A__questionmark_v_1_328) = A__questionmark_bu0_561 ) ) ) ) ).

tff(formula_180,axiom,
    ! [A__questionmark_pu0_563: c_unsorted,A__questionmark_au0_564: $int,A__questionmark_bu0_565: $int,A__questionmark_bitvectoruallocutableu0_566: c_unsorted] :
    ? [A__questionmark_v_1_330: c_sorted,A__questionmark_v_0_331: c_sorted] :
      ( ( A__questionmark_v_1_330 = c_sort(pointer(c_unit),A__questionmark_pu0_563) )
      & ( A__questionmark_v_0_331 = c_sort(alloc_table(c_unit),A__questionmark_bitvectoruallocutableu0_566) )
      & ( valid_bitvector_struct_void_P(A__questionmark_v_1_330,A__questionmark_au0_564,A__questionmark_bu0_565,A__questionmark_v_0_331)
      <=> ( ( offset_min(A__questionmark_v_0_331,A__questionmark_v_1_330) = A__questionmark_au0_564 )
          & ( offset_max(A__questionmark_v_0_331,A__questionmark_v_1_330) = A__questionmark_bu0_565 ) ) ) ) ).

tff(formula_181,axiom,
    ! [A__questionmark_pu0_567: c_unsorted,A__questionmark_au0_568: $int,A__questionmark_bu0_569: $int,A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_570: c_unsorted] :
    ? [A__questionmark_v_1_332: c_sorted,A__questionmark_v_0_333: c_sorted] :
      ( ( A__questionmark_v_1_332 = c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_pu0_567) )
      & ( A__questionmark_v_0_333 = c_sort(alloc_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_570) )
      & ( valid_root___anonstruct_T_CompositionPage_1(A__questionmark_v_1_332,A__questionmark_au0_568,A__questionmark_bu0_569,A__questionmark_v_0_333)
      <=> ( $lesseq(offset_min(A__questionmark_v_0_333,A__questionmark_v_1_332),A__questionmark_au0_568)
          & $greatereq(offset_max(A__questionmark_v_0_333,A__questionmark_v_1_332),A__questionmark_bu0_569) ) ) ) ).

tff(formula_182,axiom,
    ! [A__questionmark_pu0_571: c_unsorted,A__questionmark_au0_572: $int,A__questionmark_bu0_573: $int,A__questionmark_charuPuallocutableu0_574: c_unsorted] :
    ? [A__questionmark_v_1_334: c_sorted,A__questionmark_v_0_335: c_sorted] :
      ( ( A__questionmark_v_1_334 = c_sort(pointer(char_P),A__questionmark_pu0_571) )
      & ( A__questionmark_v_0_335 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_574) )
      & ( valid_root_char_P(A__questionmark_v_1_334,A__questionmark_au0_572,A__questionmark_bu0_573,A__questionmark_v_0_335)
      <=> ( $lesseq(offset_min(A__questionmark_v_0_335,A__questionmark_v_1_334),A__questionmark_au0_572)
          & $greatereq(offset_max(A__questionmark_v_0_335,A__questionmark_v_1_334),A__questionmark_bu0_573) ) ) ) ).

tff(formula_183,axiom,
    ! [A__questionmark_pu0_575: c_unsorted,A__questionmark_au0_576: $int,A__questionmark_bu0_577: $int,A__questionmark_charuuxuu1uuPuallocutableu0_578: c_unsorted] :
    ? [A__questionmark_v_1_336: c_sorted,A__questionmark_v_0_337: c_sorted] :
      ( ( A__questionmark_v_1_336 = c_sort(pointer(char__x__1__P),A__questionmark_pu0_575) )
      & ( A__questionmark_v_0_337 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_578) )
      & ( valid_root_char__x__1__P(A__questionmark_v_1_336,A__questionmark_au0_576,A__questionmark_bu0_577,A__questionmark_v_0_337)
      <=> ( $lesseq(offset_min(A__questionmark_v_0_337,A__questionmark_v_1_336),A__questionmark_au0_576)
          & $greatereq(offset_max(A__questionmark_v_0_337,A__questionmark_v_1_336),A__questionmark_bu0_577) ) ) ) ).

tff(formula_184,axiom,
    ! [A__questionmark_pu0_579: c_unsorted,A__questionmark_au0_580: $int,A__questionmark_bu0_581: $int,A__questionmark_voiduPuallocutableu0_582: c_unsorted] :
    ? [A__questionmark_v_1_338: c_sorted,A__questionmark_v_0_339: c_sorted] :
      ( ( A__questionmark_v_1_338 = c_sort(pointer(void_P),A__questionmark_pu0_579) )
      & ( A__questionmark_v_0_339 = c_sort(alloc_table(void_P),A__questionmark_voiduPuallocutableu0_582) )
      & ( valid_root_void_P(A__questionmark_v_1_338,A__questionmark_au0_580,A__questionmark_bu0_581,A__questionmark_v_0_339)
      <=> ( $lesseq(offset_min(A__questionmark_v_0_339,A__questionmark_v_1_338),A__questionmark_au0_580)
          & $greatereq(offset_max(A__questionmark_v_0_339,A__questionmark_v_1_338),A__questionmark_bu0_581) ) ) ) ).

tff(formula_185,axiom,
    ! [A__questionmark_pu0_583: c_unsorted,A__questionmark_au0_584: $int,A__questionmark_bu0_585: $int,A__questionmark_charuPuallocutableu0_586: c_unsorted] :
    ? [A__questionmark_v_1_340: c_sorted,A__questionmark_v_0_341: c_sorted] :
      ( ( A__questionmark_v_1_340 = c_sort(pointer(char_P),A__questionmark_pu0_583) )
      & ( A__questionmark_v_0_341 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_586) )
      & ( valid_struct_char_P(A__questionmark_v_1_340,A__questionmark_au0_584,A__questionmark_bu0_585,A__questionmark_v_0_341)
      <=> ( $lesseq(offset_min(A__questionmark_v_0_341,A__questionmark_v_1_340),A__questionmark_au0_584)
          & $greatereq(offset_max(A__questionmark_v_0_341,A__questionmark_v_1_340),A__questionmark_bu0_585) ) ) ) ).

tff(formula_186,axiom,
    ! [A__questionmark_pu0_587: c_unsorted,A__questionmark_au0_588: $int,A__questionmark_bu0_589: $int,A__questionmark_charuPuallocutableu0_590: c_unsorted,A__questionmark_charuuxuu1uuPuallocutableu0_591: c_unsorted,A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_592: c_unsorted] :
    ? [A__questionmark_v_2_342: c_type,A__questionmark_v_1_343: c_sorted,A__questionmark_v_4_344: c_sorted,A__questionmark_v_0_345: c_sorted] :
      ( ( A__questionmark_v_2_342 = pointer(char_P) )
      & ( A__questionmark_v_1_343 = c_sort(pointer(char__x__1__P),A__questionmark_pu0_587) )
      & ( A__questionmark_v_4_344 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_590) )
      & ( A__questionmark_v_0_345 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_591) )
      & ? [A__questionmark_v_3_346: c_sorted] :
          ( ( A__questionmark_v_3_346 = c_sort(memory(char__x__1__P,A__questionmark_v_2_342),A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_592) )
          & ( valid_struct_char__x__1__P(A__questionmark_v_1_343,A__questionmark_au0_588,A__questionmark_bu0_589,A__questionmark_v_4_344,A__questionmark_v_0_345,A__questionmark_v_3_346)
          <=> ( $lesseq(offset_min(A__questionmark_v_0_345,A__questionmark_v_1_343),A__questionmark_au0_588)
              & $greatereq(offset_max(A__questionmark_v_0_345,A__questionmark_v_1_343),A__questionmark_bu0_589)
              & valid_struct_char_P(c_sort(A__questionmark_v_2_342,smtlib__select(A__questionmark_v_3_346,A__questionmark_v_1_343)),0,9,A__questionmark_v_4_344) ) ) ) ) ).

tff(formula_187,axiom,
    ! [A__questionmark_pu0_593: c_unsorted,A__questionmark_au0_594: $int,A__questionmark_bu0_595: $int,A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_596: c_unsorted,A__questionmark_charuPuallocutableu0_597: c_unsorted,A__questionmark_charuuxuu1uuPuallocutableu0_598: c_unsorted,A__questionmark_uuanonstructuTuCompositionPageu1uTexteu0_599: c_unsorted,A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_600: c_unsorted] :
    ? [A__questionmark_v_2_347: c_type,A__questionmark_v_1_348: c_sorted,A__questionmark_v_0_349: c_sorted,A__questionmark_v_4_350: c_sorted,A__questionmark_v_5_351: c_sorted] :
      ( ( A__questionmark_v_2_347 = pointer(char__x__1__P) )
      & ( A__questionmark_v_1_348 = c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_pu0_593) )
      & ( A__questionmark_v_0_349 = c_sort(alloc_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_uuanonstructuTuCompositionPageu1uallocutableu0_596) )
      & ( A__questionmark_v_4_350 = c_sort(alloc_table(char_P),A__questionmark_charuPuallocutableu0_597) )
      & ( A__questionmark_v_5_351 = c_sort(alloc_table(char__x__1__P),A__questionmark_charuuxuu1uuPuallocutableu0_598) )
      & ? [A__questionmark_v_3_352: c_sorted,A__questionmark_v_6_353: c_sorted] :
          ( ( A__questionmark_v_3_352 = c_sort(memory(smtlib____anonstruct_T_CompositionPage_1,A__questionmark_v_2_347),A__questionmark_uuanonstructuTuCompositionPageu1uTexteu0_599) )
          & ( A__questionmark_v_6_353 = c_sort(memory(char__x__1__P,pointer(char_P)),A__questionmark_charuuxuu1uuPucharuuxuu1uuMu0_600) )
          & ( valid_struct___anonstruct_T_CompositionPage_1(A__questionmark_v_1_348,A__questionmark_au0_594,A__questionmark_bu0_595,A__questionmark_v_0_349,A__questionmark_v_4_350,A__questionmark_v_5_351,A__questionmark_v_3_352,A__questionmark_v_6_353)
          <=> ( $lesseq(offset_min(A__questionmark_v_0_349,A__questionmark_v_1_348),A__questionmark_au0_594)
              & $greatereq(offset_max(A__questionmark_v_0_349,A__questionmark_v_1_348),A__questionmark_bu0_595)
              & valid_struct_char__x__1__P(c_sort(A__questionmark_v_2_347,smtlib__select(A__questionmark_v_3_352,A__questionmark_v_1_348)),0,9,A__questionmark_v_4_350,A__questionmark_v_5_351,A__questionmark_v_6_353) ) ) ) ) ).

tff(formula_188,axiom,
    ! [A__questionmark_pu0_601: c_unsorted,A__questionmark_au0_602: $int,A__questionmark_bu0_603: $int,A__questionmark_voiduPuallocutableu0_604: c_unsorted] :
    ? [A__questionmark_v_1_354: c_sorted,A__questionmark_v_0_355: c_sorted] :
      ( ( A__questionmark_v_1_354 = c_sort(pointer(void_P),A__questionmark_pu0_601) )
      & ( A__questionmark_v_0_355 = c_sort(alloc_table(void_P),A__questionmark_voiduPuallocutableu0_604) )
      & ( valid_struct_void_P(A__questionmark_v_1_354,A__questionmark_au0_602,A__questionmark_bu0_603,A__questionmark_v_0_355)
      <=> ( $lesseq(offset_min(A__questionmark_v_0_355,A__questionmark_v_1_354),A__questionmark_au0_602)
          & $greatereq(offset_max(A__questionmark_v_0_355,A__questionmark_v_1_354),A__questionmark_bu0_603) ) ) ) ).

tff(formula_189,axiom,
    int_of_tag(c_sort(tag_id(void_P),void_P_tag)) = 1 ).

tff(formula_190,axiom,
    ! [A__questionmark_xu563_605: c_unsorted] :
    ? [A__questionmark_v_0_356: c_type] :
      ( ( A__questionmark_v_0_356 = pointer(void_P) )
      & ? [A__questionmark_v_1_357: c_sorted] :
          ( ( A__questionmark_v_1_357 = c_sort(A__questionmark_v_0_356,A__questionmark_xu563_605) )
          & ( c_sort(A__questionmark_v_0_356,void_P_of_bitvector(c_sort(bitvector,bitvector_of_void_P(A__questionmark_v_1_357)))) = A__questionmark_v_1_357 ) ) ) ).

tff(formula_191,axiom,
    ! [A__questionmark_pu564_606: c_unsorted] :
    ? [A__questionmark_v_0_358: c_type] :
      ( ( A__questionmark_v_0_358 = pointer(void_P) )
      & ? [A__questionmark_v_1_359: c_sorted] :
          ( ( A__questionmark_v_1_359 = c_sort(A__questionmark_v_0_358,A__questionmark_pu564_606) )
          & ( A__questionmark_v_1_359 = c_sort(A__questionmark_v_0_358,void_P_of_pointer_address(c_sort(pointer(c_unit),pointer_address(A__questionmark_v_1_359)))) ) ) ) ).

tff(formula_192,axiom,
    ? [A__questionmark_v_0_360: c_type] :
      ( ( A__questionmark_v_0_360 = tag_id(void_P) )
      & parenttag(c_sort(A__questionmark_v_0_360,void_P_tag),c_sort(A__questionmark_v_0_360,bottom_tag)) ) ).

tff(formula_193,axiom,
    ! [A__questionmark_xu566_607: c_unsorted,A__questionmark_voiduPutagutableu565_608: c_unsorted] : instanceof(c_sort(tag_table(void_P),A__questionmark_voiduPutagutableu565_608),c_sort(pointer(void_P),A__questionmark_xu566_607),c_sort(tag_id(void_P),void_P_tag)) ).

tff(formula_194,axiom,
    ~ ! [A__questionmark_smtlib____anonstruct_T_CompositionPage_1_Page_1_alloc_table: c_unsorted,A__questionmark_smtlib____anonstruct_T_CompositionPage_1_Texte_Page_1: c_unsorted,A__questionmark_char__x__1__P_char__x__1__M_Page_1: c_unsorted] :
      ? [A__questionmark_v_0_361: c_type,A__questionmark_v_1_362: c_type] :
        ( ( A__questionmark_v_0_361 = pointer(char_P) )
        & ( A__questionmark_v_1_362 = pointer(char__x__1__P) )
        & ( ( ( c_Boolean_true = c_Boolean_true )
            & valid_Page(c_sort(alloc_table(smtlib____anonstruct_T_CompositionPage_1),A__questionmark_smtlib____anonstruct_T_CompositionPage_1_Page_1_alloc_table)) )
         => eq_message(c_sort(A__questionmark_v_0_361,smtlib__select(c_sort(memory(char__x__1__P,A__questionmark_v_0_361),A__questionmark_char__x__1__P_char__x__1__M_Page_1),c_sort(A__questionmark_v_1_362,shift(c_sort(A__questionmark_v_1_362,smtlib__select(c_sort(memory(smtlib____anonstruct_T_CompositionPage_1,A__questionmark_v_1_362),A__questionmark_smtlib____anonstruct_T_CompositionPage_1_Texte_Page_1),c_sort(pointer(smtlib____anonstruct_T_CompositionPage_1),'Page'))),9)))),0) ) ) ).

%------------------------------------------------------------------------------
