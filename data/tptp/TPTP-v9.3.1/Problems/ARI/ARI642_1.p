%------------------------------------------------------------------------------
% File     : ARI642_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Example 23
% Version  : Especial.
% English  :

% Refs     : [ALR14] Avigad et al. (2014), A Heuristic Prover for Real Ineq
%          : [LAR14] Lewis et al. (2014), A Heuristic Prover for Real Inequ
%          : [Lew14] Lewis (2014), Email to Geoff Sutcliffe
% Source   : [Lew14]
% Names    : Example 23 [Lew14]

% Status   : Theorem
% Rating   : 0.75 v9.1.0, 0.80 v9.0.0, 0.75 v8.2.0, 0.83 v7.5.0, 1.00 v7.4.0, 0.67 v7.3.0, 0.75 v7.1.0, 0.67 v7.0.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :   10 (   4 unt;   5 typ;   0 def)
%            Number of atoms       :    6 (   0 equ)
%            Maximal formula atoms :    2 (   1 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   1 avg)
%            Maximal term depth    :    5 (   2 avg)
%            Number arithmetic     :   27 (   6 atm;  14 fun;   6 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   12 (   5 usr;   7 con; 0-2 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
%----Should be known property Axiom: Forall([x], ceil(x) >= x)
tff(m_type,type,
    m: $real ).

tff(x_type,type,
    x: $real ).

tff(a_type,type,
    a: $real ).

tff(b_type,type,
    b: $real ).

tff(f_type,type,
    f: $real > $real ).

tff(ceiling_property,axiom,
    ! [M: $real] :
      ( $greater(M,0.0)
     => $less(f($ceiling(M)),$sum(a,$product($quotient(1.0,$ceiling(M)),$sum($product(-1.0,a),b)))) ) ).

tff(hypothesis,hypothesis,
    $less(a,b) ).

tff(hypothesis_01,hypothesis,
    $greater(x,a) ).

tff(hypothesis_02,hypothesis,
    $greatereq(m,$product($quotient(1.0,$sum($product(-1.0,a),x)),$sum($product(-1.0,a),b))) ).

tff(conclusion,conjecture,
    $less(f($ceiling(m)),x) ).

%------------------------------------------------------------------------------
