# Repository-owned exceptions

## Read this when

A change claims an owner-defined exemption from definitions or work orders.

## Before this action

Identify the selected release and read Availability below.

## Availability

Repository owners may configure only whether a change needs formal definitions
and work orders. Lifecycle rules and required gates remain fixed. The selected
release does not provide an owner-configured exception evaluator. Repository
prose or a documentation path is not proof that an exception applies.

## Procedure

**Inputs:** The requested change and claimed owner exception.

**Output:** No formal artifact or repository file. A transient applicability
finding naming the selected evaluator and its missing capability.

**Actions:** Confirm the selected evaluator identity through [SETUP.md#procedure](SETUP.md#procedure).
Report that this release cannot evaluate the claimed exception. Use the ordinary
governed definition and work-order procedure. Do not accept a red required check,
invent a work-order ID or waive a lifecycle gate. A later released exception
capability requires its own supported procedure and explicit adoption.

**Harness commands:** No exception command is available in this release.

**Completion:** The unsupported claim is explicit and the governed fallback is selected.

**Later use:** [DEFINE_CHANGE.md#procedure](DEFINE_CHANGE.md#procedure) supplies that fallback.

## Read next when

The exception is unavailable → [DEFINE_CHANGE.md](DEFINE_CHANGE.md#procedure).
